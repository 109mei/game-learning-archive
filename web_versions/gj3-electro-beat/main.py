# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---
import asyncio

import pygame
import random
import math
import sys
from collections import deque

# --- 設定 ---
WIDTH, HEIGHT = 960, 600
FPS = 60
GRAVITY = 0.8
GROUND_Y = HEIGHT - 80

# ゲームパラメータ
ENEMY_SPAWN_INTERVAL = 60  # 秒
MAX_TURNS = 5
BOSS_BASE_HEARTS = 1

# 色
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (150,150,150)
RED = (220,50,50)
GREEN = (80,180,80)
YELLOW = (240,220,60)
BLUE = (60,140,240)
ORANGE = (255,140,0)

# --- ユーティリティ ---

def clamp(x, a, b):
    return max(a, min(b, x))

# --- クラス ---
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 48
        self.h = 64
        self.vx = 0
        self.vy = 0
        self.speed = 4
        self.on_ground = False
        self.hp = 5
        self.max_hp = 5
        self.invincible_timer = 0
        self.color = BLUE
        # 攻撃関係
        self.attack_power = 1
        self.item_gauge = 0
        self.max_item_gauge = 10
        self.available_attacks = 1

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        # 物理
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy
        # 地面判定
        if self.y + self.h >= GROUND_Y:
            self.y = GROUND_Y - self.h
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False
        # 摩擦
        self.vx *= 0.9
        # invincible
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def jump(self):
        if self.on_ground:
            self.vy = -12
            self.on_ground = False

    def move_right(self):
        self.vx += self.speed
        self.vx = clamp(self.vx, -10, 10)

    def move_left(self):
        self.vx -= self.speed
        self.vx = clamp(self.vx, -10, 10)

    def take_damage(self, dmg):
        if self.invincible_timer <= 0:
            self.hp -= dmg
            self.invincible_timer = FPS * 1  # 1秒無敵
            # 点滅などは描画で反映
            if self.hp < 0:
                self.hp = 0

    def pick_item(self, val=1):
        self.item_gauge += val
        if self.item_gauge >= self.max_item_gauge:
            self.item_gauge -= self.max_item_gauge
            self.available_attacks += 1
            self.attack_power += 1

class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 12
        self.vx = random.uniform(-2,2)
        self.vy = random.uniform(-6,-2)
        self.bounce = 0.7
        self.collected = False
        self.color = YELLOW

    def update(self):
        self.vy += GRAVITY * 0.6
        self.x += self.vx
        self.y += self.vy
        # 地面バウンド
        if self.y + self.r >= GROUND_Y:
            self.y = GROUND_Y - self.r
            self.vy = -abs(self.vy) * self.bounce
            # 摩擦で横減速
            self.vx *= 0.8
        # 壁は画面端で反転
        if self.x - self.r <= 0 or self.x + self.r >= WIDTH:
            self.vx *= -1

    def rect(self):
        return pygame.Rect(self.x-self.r, self.y-self.r, self.r*2, self.r*2)

class Enemy:
    def __init__(self, x, y, hp=10):
        self.x = x
        self.y = y
        self.w = 48
        self.h = 48
        self.vx = random.choice([-2,-1,1,2])
        self.vy = 0
        self.hp = hp
        self.max_hp = hp
        self.color = RED

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        # 簡易ランダム移動
        if random.random() < 0.02:
            self.vx = random.uniform(-3,3)
        self.x += self.vx
        # 地面保持
        if self.x < 0: self.x = 0; self.vx *= -1
        if self.x + self.w > WIDTH: self.x = WIDTH - self.w; self.vx *= -1

class Boss:
    def __init__(self):
        self.x = WIDTH//2 - 80
        self.y = 60
        self.w = 160
        self.h = 120
        self.base_hearts = BOSS_BASE_HEARTS
        self.turn = 0
        self.max_hp = 30
        self.hp = self.max_hp
        self.color = ORANGE
        self.alive = True

    def increase_turn(self):
        self.turn += 1
        # ハート（HP量）を増やす
        add = 10 + self.turn * 5
        self.max_hp += add
        self.hp = self.max_hp

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

# --- エフェクト ---
class Effect:
    def __init__(self, kind, x, y, life=30):
        self.kind = kind
        self.x = x
        self.y = y
        self.life = life

    def update(self):
        self.life -= 1

# --- リズムミニゲーム ---
class RhythmGame:
    def __init__(self, beats=8, interval=0.8):
        self.beats = beats
        self.interval = interval
        self.current = 0
        self.timer = 0.0
        self.active = False
        self.success = 0
        # timing window (sec)
        self.window = 0.25
        self.beat_times = []

    def start(self):
        self.active = True
        self.timer = 0.0
        self.current = 0
        self.success = 0
        self.beat_times = [i*self.interval for i in range(self.beats)]

    def update(self, dt):
        if not self.active: return
        self.timer += dt
        if self.timer > self.beat_times[-1] + 1.0:
            self.active = False

    def press(self):
        # 判定: 現在のtimerと最も近いビートを比較
        if not self.active: return False
        t = self.timer
        diffs = [abs(t - bt) for bt in self.beat_times]
        m = min(diffs)
        if m <= self.window:
            self.success += 1
            return True
        return False

# --- メインゲーム ---

async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("One-Button Game (Prototype)")
    clock = pygame.time.Clock()

    # TODO: ここにBGMや効果音を配置（コメントアウト）
    # pygame.mixer.init()
    # bgm = pygame.mixer.Sound('bgm.ogg')
    # sfx_jump = pygame.mixer.Sound('jump.wav')
    # sfx_pick = pygame.mixer.Sound('pick.wav')

    # ゲーム状態
    state = 'start'  # start, explain, playing, boss_rhythm, gameover, clear
    player = Player(120, GROUND_Y - 64)
    items = []
    enemies = []
    effects = []
    boss = Boss()

    last_enemy_spawn = 0.0
    total_time = 0.0
    turn = 0

    rhythm = RhythmGame(beats=6, interval=0.7)

    # 入力測定用
    pressing = False
    press_start = 0.0

    # UIフォント
    font = pygame.font.Font("_webfont.ttf", 20)
    big_font = pygame.font.Font("_webfont.ttf", 44)

    # START画面用アニメ
    title_bob = 0.0

    # テスト用に最初にいくつかアイテムを置く
    for i in range(3):
        items.append(Item(random.randint(100, WIDTH-100), random.randint(50, 200)))

    while True:
        await asyncio.sleep(0)
        dt = clock.get_time() / 1000.0
        total_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                if state == 'start':
                    state = 'explain'
                elif state == 'explain':
                    state = 'playing'
                    last_enemy_spawn = total_time
                elif state == 'playing':
                    # スペース・クリックの押下開始
                    pressing = True
                    press_start = total_time
                elif state == 'boss_rhythm':
                    # リズムゲームでの押下
                    if rhythm.press():
                        # 成功
                        dmg = 5 + player.attack_power
                        boss.take_damage(dmg)
                        effects.append(Effect('rhythm_hit', boss.x + boss.w//2, boss.y + boss.h//2, life=20))
                elif state in ('gameover', 'clear'):
                    # リスタート
                    player = Player(120, GROUND_Y - 64)
                    items.clear(); enemies.clear(); effects.clear(); boss = Boss()
                    last_enemy_spawn = total_time
                    turn = 0
                    state = 'start'
            elif event.type == pygame.MOUSEBUTTONUP or (event.type == pygame.KEYUP and event.key == pygame.K_SPACE):
                if state == 'playing' and pressing:
                    pressing = False
                    hold = total_time - press_start
                    # 敵がいない -> 操作は移動/ジャンプ
                    if len(enemies) == 0:
                        if hold < 0.25:
                            player.jump()
                            # sfx_jump.play()
                        elif hold < 0.6:
                            player.move_right()
                        else:
                            player.move_left()
                    else:
                        # 敵がいる（戦闘モード） -> 攻撃
                        if hold < 0.25:
                            # ライト攻撃
                            dmg = player.attack_power
                            # 攻撃範囲の判定 (円)
                            attack_x = player.x + player.w//2
                            attack_y = player.y + player.h//2
                            effects.append(Effect('light', attack_x, attack_y, life=18))
                            # 範囲内の敵にダメージ
                            for e in enemies:
                                dist = math.hypot((e.x+e.w/2)-attack_x, (e.y+e.h/2)-attack_y)
                                if dist < 120:
                                    e.hp -= dmg
                        else:
                            dmg = player.attack_power * 2
                            effects.append(Effect('heavy', player.x+player.w//2, player.y, life=30))
                            for e in enemies:
                                dist = math.hypot((e.x+e.w/2)-(player.x+player.w/2), (e.y+e.h/2)-(player.y+player.h/2))
                                if dist < 160:
                                    e.hp -= dmg

        # --- ゲーム更新 ---
        if state == 'explain':
            pass
        elif state == 'playing':
            # スポーン判定（1分ごと）
            if total_time - last_enemy_spawn >= ENEMY_SPAWN_INTERVAL and turn < MAX_TURNS:
                # 敵を湧かせる
                num = 1 + turn  # ターンが進むごとに敵の数/強さ増
                enemies = [Enemy(random.randint(400, WIDTH-100), GROUND_Y-48, hp=8+turn*5) for _ in range(num)]
                last_enemy_spawn = total_time
                turn += 1
                # ボスのターン増加
                boss.increase_turn()

            # 通常更新
            player.update()
            for it in items:
                it.update()
                # プレイヤー接触
                if it.rect().colliderect(player.rect()) and not it.collected:
                    it.collected = True
                    player.pick_item(1)
                    # sfx_pick.play()
            items = [it for it in items if not it.collected]

            for e in enemies:
                e.update()
                # 敵とプレイヤーの当たり判定
                if e.rect().colliderect(player.rect()):
                    player.take_damage(1)

            enemies = [e for e in enemies if e.hp > 0]

            # 敵を全部倒したらアイテムドロップ
            if len(enemies) == 0 and turn > 0 and state == 'playing' and random.random() < 0.02:
                # ランダムにアイテム湧く
                items.append(Item(random.randint(100, WIDTH-100), random.randint(50, 200)))

            # エフェクト更新
            for ef in effects:
                ef.update()
            effects = [ef for ef in effects if ef.life > 0]

            # 敵が湧いた状態で一定ターン経過後にボスリズムへ
            if turn >= MAX_TURNS and boss.alive:
                state = 'boss_rhythm'
                rhythm.start()

            # 制限時間表示やゲームオーバー判定
            if player.hp <= 0:
                state = 'gameover'

        elif state == 'boss_rhythm':
            rhythm.update(dt)
            # プレイヤーの通常更新は継続
            player.update()
            for it in items:
                it.update()
                if it.rect().colliderect(player.rect()) and not it.collected:
                    it.collected = True
                    player.pick_item(1)
            items = [it for it in items if not it.collected]

            # リズムが終わったらボスにダメージ判定
            if not rhythm.active:
                # 成功数に応じて追加ダメージ
                dmg = rhythm.success * (1 + player.attack_power//2)
                boss.take_damage(dmg)
                # リズム終了後は通常に戻すか、もう一度リズムにする
                if boss.alive:
                    state = 'playing'
                else:
                    state = 'clear'

        # --- 描画 ---
        screen.fill((22,22,30))

        if state == 'start':
            title_bob += dt * 2
            title_y = HEIGHT//2 - 60 + math.sin(title_bob) * 8
            draw_text_center(screen, big_font, "ONE-BUTTON ADVENTURE", WIDTH//2, title_y, WHITE)
            draw_text_center(screen, font, "Click or press SPACE to start", WIDTH//2, HEIGHT//2 + 40, GRAY)
        elif state == 'explain':
            draw_text_center(screen, big_font, "ルール説明", WIDTH//2, 80, WHITE)
            lines = [
                "ワンボタンで遊ぶアクションゲーム",
                "- タップ: ジャンプ (敵がいないとき)",
                "- 短いホールド: 右に移動",
                "- 長いホールド: 左に移動",
                "- 敵が湧くとボタンは攻撃に変化",
                "  タップ: ライト攻撃, ホールド: ヘヴィ攻撃",
                "- アイテムを集めて攻撃力UP / 技をアンロック",
                "- 5ターン経過後にボス戦（リズムミニゲーム）",
                "Click/SPACEでゲーム開始"
            ]
            y = 140
            for l in lines:
                draw_text_center(screen, font, l, WIDTH//2, y, WHITE)
                y += 28
        else:
            # 背景 / 地面
            pygame.draw.rect(screen, (40,40,60), (0,0,WIDTH,HEIGHT))
            pygame.draw.rect(screen, (30,20,10), (0, GROUND_Y, WIDTH, HEIGHT-GROUND_Y))

            # アイテム
            for it in items:
                pygame.draw.circle(screen, it.color, (int(it.x), int(it.y)), it.r)

            # プレイヤー
            pr = player.rect()
            col = player.color
            # 点滅 (無敵時)
            if player.invincible_timer > 0 and (player.invincible_timer//6)%2==0:
                col = (200,200,200)
            pygame.draw.rect(screen, col, pr)

            # エフェクト (シンプル)
            for ef in effects:
                if ef.kind == 'light':
                    r = 40 + (30 - ef.life)
                    pygame.draw.circle(screen, (255,200,120), (int(ef.x), int(ef.y)), int(r), 3)
                elif ef.kind == 'heavy':
                    r = 20 + (30 - ef.life)*3
                    pygame.draw.circle(screen, (255,120,120), (int(ef.x), int(ef.y)), int(r), 0)
                elif ef.kind == 'rhythm_hit':
                    pygame.draw.circle(screen, (255,255,100), (int(ef.x), int(ef.y)), max(1, ef.life), 2)

            # 敵
            for e in enemies:
                pygame.draw.rect(screen, e.color, e.rect())
                # HPバー
                draw_bar(screen, e.x, e.y-8, e.w, 6, e.hp, e.max_hp)

            # ボス
            if boss.alive:
                pygame.draw.rect(screen, boss.color, boss.rect())
                # ボスHPバー
                draw_bar(screen, boss.x, boss.y-12, boss.w, 12, boss.hp, boss.max_hp)
                draw_text(screen, font, f"Boss Turn:{boss.turn}", boss.x+6, boss.y+boss.h+6, WHITE)

            # UI: HPハート表示
            draw_hearts(screen, 16, 16, player.hp, player.max_hp)

            # タイマー（画面右上）
            draw_text(screen, font, f"Time: {int(total_time)}s", WIDTH-140, 16, WHITE)

            # アイテムゲージ
            draw_gauge(screen, 16, 60, 200, 16, player.item_gauge, player.max_item_gauge, "Item")
            draw_gauge(screen, 16, 86, 200, 16, player.attack_power, 20, "Attack")

            # 使用可能攻撃数
            draw_text(screen, font, f"Attacks: {player.available_attacks}", 16, 110, WHITE)

            # リズム状態
            if state == 'boss_rhythm':
                draw_text_center(screen, big_font, "BOSS RHYTHM! Press in time", WIDTH//2, 200, YELLOW)
                # ビートの進行表示
                for i, bt in enumerate(rhythm.beat_times):
                    x = WIDTH//2 - 200 + i*60
                    y = 260
                    color = GRAY
                    if rhythm.timer >= bt:
                        color = GREEN
                    pygame.draw.circle(screen, color, (x,y), 18)

        # ゲームオーバー / クリア
        if state == 'gameover':
            draw_text_center(screen, big_font, "GAME OVER", WIDTH//2, HEIGHT//2 - 20, RED)
            draw_text_center(screen, font, "Click/SPACE to restart", WIDTH//2, HEIGHT//2 + 40, GRAY)
        elif state == 'clear':
            draw_text_center(screen, big_font, "YOU WIN!", WIDTH//2, HEIGHT//2 - 20, GREEN)
            draw_text_center(screen, font, "Click/SPACE to restart", WIDTH//2, HEIGHT//2 + 40, GRAY)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

# --- 描画ヘルパー ---

def draw_text(surface, font, text, x, y, color):
    surf = font.render(str(text), True, color)
    surface.blit(surf, (x, y))

def draw_text_center(surface, font, text, x, y, color):
    surf = font.render(str(text), True, color)
    r = surf.get_rect()
    r.center = (x,y)
    surface.blit(surf, r.topleft)

def draw_bar(surface, x, y, w, h, val, maxv):
    pygame.draw.rect(surface, (60,60,60), (x,y,w,h))
    if maxv>0:
        rw = int(w * (val/maxv))
        pygame.draw.rect(surface, (100,220,140), (x,y,rw,h))
        pygame.draw.rect(surface, WHITE, (x,y,w,h), 1)

def draw_gauge(surface, x, y, w, h, val, maxv, label=''):
    draw_text(surface, pygame.font.Font("_webfont.ttf", 16), label, x, y-18, WHITE)
    draw_bar(surface, x, y, w, h, val, maxv)

def draw_hearts(surface, x, y, hp, max_hp):
    # ハートを簡易図形で描く
    for i in range(max_hp):
        hx = x + i*28
        hy = y
        rect = pygame.Rect(hx, hy, 22, 22)
        if i < hp:
            pygame.draw.polygon(surface, RED, [(hx+11,hy),(hx+22,hy+11),(hx+11,hy+22),(hx,hy+11)])
        else:
            pygame.draw.polygon(surface, GRAY, [(hx+11,hy),(hx+22,hy+11),(hx+11,hy+22),(hx,hy+11)])


async def _web_main():
    if __name__ == '__main__':
        await main()



asyncio.run(_web_main())