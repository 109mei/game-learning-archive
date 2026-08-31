# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---
import asyncio
# coding: utf-8
import sys
pass  # web: import numpy 無効化
import time
import random
import pygame
from pygame.locals import *
import os
import math  # タイトル揺れなどのアニメーションに利用

# -----------------------------
#  初期設定
# -----------------------------
pygame.init()

# DPIまわり（Windows でボケないようにする）
if sys.platform == "win32":
    pass  # web: ctypes無効化 | import ctypes
    pass  # web: ctypes無効化 | ctypes.windll.user32.SetProcessDPIAware()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
else:
    os.environ['SDL_VIDEO_CENTERED'] = '1'

# フォント（日本語表示用）
FONT_PATH = "NotoSansJP-Regular.ttf"
FONT_SIZE = 28
font_default = pygame.font.Font(FONT_PATH, FONT_SIZE)

# 画面サイズ
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0)
pygame.display.set_caption("SwitchQuiz")

clock = pygame.time.Clock()

# -----------------------------
#  画像・音の読み込み
# -----------------------------
# 背景画像（なくても動く）
bg_path = os.path.join("画像", "背景.jpg")
if os.path.exists(bg_path):
    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
else:
    background = None

# スコア表示用の画像
score_img = None
score_path = os.path.join("画像", "score.png")
if os.path.exists(score_path):
    try:
        score_img = pygame.image.load(score_path).convert_alpha()
    except:
        score_img = None

# サウンド：ミキサー初期化
correct_se = None
try:
    pygame.mixer.init()
    # 正解SE
    se_path = os.path.join("効果音・BGM", "twinkle.ogg")
    if os.path.exists(se_path):
        correct_se = pygame.mixer.Sound(se_path)
    # BGM
    bgm_path = os.path.join("効果音・BGM", "3.ogg")
    if os.path.exists(bgm_path):
        pygame.mixer.music.load(bgm_path)
        pygame.mixer.music.play(-1)  # ループ再生
except:
    correct_se = None

# -----------------------------
#  クイズデータ（問題・答え・解説）
# -----------------------------
QUIZ_DATA = [
    ("パンダは草食動物である。", False,
     "パンダの食性は竹や笹を主食とする雑食性だが、分類上は食肉目（肉食動物）。"),
    ("学ランの「ラン」はオランダのことである。", True,
     "学ランは『学生オランダ服』が語源。19世紀にオランダ経由で制服文化が入ったことに由来する。"),
    ("公式設定ではマリオとルイージは血がつながっていない。", False,
     "任天堂の公式設定ではマリオとルイージはれっきとした兄弟（マリオが兄）である。"),
    ("海のほとんどはまだ未解明の領域である。", True,
     "海洋の95％以上は未踏査と言われており、深海には未知の生物・地形が多数存在すると考えられている。"),
    ("南極に住民票がある人物がいる。", False,
     "南極はどの国にも属しておらず、住民票制度も存在しない。条約により軍事利用も禁止されている。"),
    ("鉛筆一本で書ける距離は約100km。", False,
     "正しくは約50km前後。メーカーによって差はあるが、100kmは誇張表現である。"),
    ("かき氷で頭が痛くなる現象は正式に『かき氷現象』と呼ばれる。", False,
     "医学的には『アイスクリーム頭痛』と呼ばれる。血管の急激な収縮と拡張が原因。"),
    ("ケンタッキーフライドチキンの秘伝レシピを知る人物は世界でごく少数しかいない。", True,
     "KFCの11種スパイスの配合は極秘とされ、関係者のごく数名のみが知っていると言われている。"),
    ("なめくじには塩だけでなく砂糖も効く。", True,
     "浸透圧の作用で体内の水分が奪われるため、砂糖でも同様の反応が起こる。"),
    ("ロッテが最初に発売した商品は使い捨てカイロである。", False,
     "ロッテの第一号商品はチューインガム。創業当初からガムの製造で知られていた。"),
    ("満腹になると聴力が上がるという科学的根拠がある。", False,
     "満腹と聴力向上に相関する科学的データは存在しない。都市伝説の一種。"),
    ("ブラジルの首都はブラジリアである。", True,
     "1960年にリオデジャネイロから遷都。国内の均衡発展を目的とした計画都市。"),
    ("シンガポールではガムの販売に規制がある。", True,
     "街の清掃問題から1992年にガムが禁止された。現在も医療用以外はほぼ販売不可。"),
    ("サハラ砂漠の『サハラ』の意味は『海』である。", False,
     "アラビア語で『砂漠』を意味する。つまり『サハラ砂漠』は『砂漠・砂漠』と重複している。"),
    ("エッフェル塔は夏と冬で高さが変化する。", True,
     "鉄は熱で膨張するため、夏と冬で約10〜20cmほど高さが変化する。"),
    ("パンケーキの『パン』は食パンの『パン』である。", False,
     "英語の『pan（フライパン）』が語源で、食パンとは無関係。"),
    ("フラミンゴの体が赤いのはエサの色素のためである。", True,
     "エビやプランクトンに含まれるβカロテン（赤い色素）が体に沈着して赤くなる。"),
    ("アンパンマンのあんはこしあんである。", False,
     "公式設定では『つぶあん』。絵本時代からの設定である。"),
    ("犬は汗をほとんどかかない。", True,
     "犬の汗腺は肉球にしかなく、体温調節は主に舌を出すパンティングで行う。"),
    ("日本の歯医者の数はコンビニより多い。", True,
     "全国の歯科医院は約7万件でコンビニより多い。過当競争が問題とされるほど。"),
    ("世界で最も飲まれている酒はウォッカである。", False,
     "最も消費量が多いのは“ビール”。ウォッカは特定地域で人気だが世界全体ではない。"),
    ("マンボウは99.99%の確率で大人になれない。", True,
     "卵を3億個以上産むが成魚になるのは極めて僅かと言われる。"),
    ("カラスは人間の顔を記憶して仲間と共有できる。", True,
     "研究により、カラスが敵対した人間の顔を仲間へ警戒情報として伝達することが確認されている。"),
    ("エベレスト山は毎年少しずつ高くなっている。", True,
     "プレートの衝突により地殻変動が続いているため、年間数ミリ〜数センチ高くなる。"),
    ("オーストラリアには氷河が存在する。", True,
     "ニューサウスウェールズ州に氷河地形があり、山岳地帯にわずかに残るとされる。"),
    ("アイスクリームは昔、薬として扱われていたことがある。", True,
     "古代ギリシャでは氷菓が熱さましの薬として処方されていた記録がある。"),
    ("ポテトチップスは客への腹いせがきっかけで生まれたと言われている。", True,
     "チップスを厚いと言って文句を言う客に対し、シェフが超薄切りで揚げたのが始まりという説が有名。"),
    ("バナナは木ではなく草の仲間である。", True,
     "バナナの幹に見える部分は偽茎であり、分類上は多年草にあたる。"),
    ("指の節を鳴らしても太くなることはない。", True,
     "関節を鳴らしても指が太くなるという科学的根拠はない。音は関節液中の気泡がはじける現象によるものとされる。"),
    ("満月の日に出生率が上がるという統計データがある。", False,
     "出生率と月齢に相関はないと複数の研究で示されている。迷信の一つ。"),
    ("自由の女神の色は元々茶色だった。", True,
     "銅製のため、完成当時は茶色だったが、酸化によって現在の緑青色になった。"),
    ("紙は中国ではなくエジプトで発明された。", False,
     "紙の発明は後漢時代の中国（蔡倫）が有名。エジプトで発明されたパピルスは『紙』ではない。"),
    ("トランプのハートの女王はジュリエットがモデルというのは誤りである。", True,
     "一般に“ユディト”がモデルとされ、ジュリエットとは無関係。"),
    ("ヨーヨーはもともと武器として使われていた。", True,
     "古代フィリピンでは狩りの武器として使用されていたとされる。"),
    ("世界最初のコンピュータウイルスはジョークとして作られた。", True,
     "1970年代のウイルスは研究実験の一環で、悪意のあるものではなかった。"),
    ("カエルは冬眠中もまったく呼吸をしない。", False,
     "皮膚呼吸で酸素を取り込むため、完全に無呼吸になるわけではない。"),
    ("イルカには匂いを感じる嗅覚がない。", True,
     "進化の過程で嗅覚器官が退化し、匂いを感じる能力をほぼ失っている。"),
    ("コーヒーは昔“悪魔の飲み物”と言われ禁止されたことがある。", True,
     "17世紀ヨーロッパで宗教的理由からコーヒーが禁じられた時期がある。"),
    ("ポップコーンは1万年前には存在していた。", True,
     "ペルーなどで1万年以上前のポップコーン化した穀物が発見されている。"),
]
# -----------------------------
#  ゲーム用の変数
# -----------------------------
SELECT_TIME = 5.0   # 1問あたりの制限時間（秒）
quiz = []           # ここにランダムで選ばれた7問が入る
q_index = 0         # 今の問題番号（0～）
score = 0           # スコア
select_is_maru = True   # Trueなら○、Falseなら×
time_left = SELECT_TIME
in_result = False   # 判定表示中フラグ
mode = "title"      # "title" / "select" / "result" / "end"

# 正解時のフラッシュ用タイマー（秒）
flash_timer = 0.0

# 問題文のアニメーション用
q_anim_timer = 0.0
Q_ANIM_DURATION = 0.6  # フェード＆ズームインにかける時間（秒）
q_surface = None
q_rect = None

# タイトル画面のアニメーション用
title_time = 0.0

# 色
BLACK = (0, 0, 0)
RED   = (255, 60, 60)
BLUE  = (60, 100, 255)
GREEN = (0, 180, 0)
GRAY  = (85, 85, 85)
WHITE = (255, 255, 255)

# -----------------------------
#  ユーティリティ関数
# -----------------------------
def wrap_text(text, font, max_width):
    """
    日本語向けの1文字ずつ改行処理
    text: 文字列
    font: pygame.font.Font
    max_width: 一行の最大幅
    """
    lines = []
    line = ""
    for ch in text:
        test_line = line + ch
        w, h = font.size(test_line)
        if w > max_width and line != "":
            lines.append(line)
            line = ch
        else:
            line = test_line
    if line:
        lines.append(line)
    return lines

def draw_rounded_rect(surface, rect, color, radius=10, width=0, border_color=None, border_width=2):
    """簡易的な角丸長方形描画"""
    x, y, w, h = rect
    # 中身
    if width == 0:
        pygame.draw.rect(surface, color, rect, border_radius=radius)
    else:
        pygame.draw.rect(surface, color, width, border_radius=radius)
    # 枠線
    if border_color is not None and border_width > 0:
        pygame.draw.rect(surface, border_color, rect, border_width, border_radius=radius)

def get_bar_color(ratio: float):
    """
    残り時間の割合 ratio(0〜1) に応じて
    緑 → 黄 → 赤 に変化する色を返す
    """
    ratio = max(0.0, min(1.0, ratio))
    green = (80, 180, 80)
    yellow = (255, 230, 0)
    red = (255, 80, 80)

    if ratio > 0.5:
        # 0.5〜1.0 : yellow → green
        t = (ratio - 0.5) / 0.5  # 0〜1
        r = int(yellow[0] + (green[0] - yellow[0]) * t)
        g = int(yellow[1] + (green[1] - yellow[1]) * t)
        b = int(yellow[2] + (green[2] - yellow[2]) * t)
    else:
        # 0.0〜0.5 : red → yellow
        t = ratio / 0.5  # 0〜1
        r = int(red[0] + (yellow[0] - red[0]) * t)
        g = int(red[1] + (yellow[1] - red[1]) * t)
        b = int(red[2] + (yellow[2] - red[2]) * t)
    return (r, g, b)

def build_question_surface(text: str):
    """
    問題文をまとめて1枚のSurfaceに描画しておき、
    あとで拡大＆フェードしながら表示するための準備をする。
    """
    global q_surface, q_rect

    font_q = pygame.font.Font(FONT_PATH, 64)  # 大きめフォント
    max_q_width = SCREEN_WIDTH - 300
    q_lines = wrap_text(text, font_q, max_q_width)

    if not q_lines:
        q_surface = None
        q_rect = None
        return

    line_height = font_q.get_linesize() + 10
    surf_w = max(font_q.size(line)[0] for line in q_lines)
    surf_h = line_height * len(q_lines)

    # 透明なSurfaceを作ってそこに行ごとに描画
    q_surface = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA).convert_alpha()
    q_surface.fill((0, 0, 0, 0))

    y = 0
    for line in q_lines:
        text_surf = font_q.render(line, True, BLACK)
        x = (surf_w - text_surf.get_width()) // 2
        q_surface.blit(text_surf, (x, y))
        y += line_height

    q_rect = q_surface.get_rect()
    q_rect.centerx = SCREEN_WIDTH // 2
    q_rect.top = 180  # 画面中央より少し上

def get_rank_comment(score, total):
    """
    スコアに応じてランクとコメントを返す。
    ⑥ 終了画面のランク演出
    """
    if total <= 0:
        return "C", "まだまだこれから！まずは1問ずつ覚えていこう。"

    ratio = score / total
    if score == total:
        return "S", "全問正解！クイズマスター誕生！"
    elif ratio >= 0.7:
        return "A", "かなりの物知り！もう一歩でコンプリート！"
    elif ratio >= 0.4:
        return "B", "なかなか健闘しました。あと少し頑張ろう！"
    else:
        return "C", "ここから知識を増やしていこう！"

# -----------------------------
#  メインループ
# -----------------------------
running = True

async def _web_main():
    global alpha, bar_color, bar_h, bar_margin_x, bar_w, bar_w_full, bar_x, bar_y, base_top, base_y, blink_on, box_h, box_w, box_x, box_y, color, comment, comment_surf, correct_answer, dt, end_text, event, expl_lines, flash_timer, font_big, font_expl, font_mid, font_rank, font_score, font_small, hint, in_result, info1, info2, info3, is_correct, k, line, margin, mode, new_h, new_w, offset_y, q_anim_timer, q_ans, q_expl, q_index, q_text, quiz, r, r_x, r_y, rank, rank_surf, ratio, rect, restart_text, result_color, result_text, running, s, s_x, s_y, scale, scaled, score, score_label, score_text, score_text_main, score_x, select_is_maru, surf, sx, sy, symbol, t, text_y, time_left, title, title_ex, title_time, title_x, title_y, total
    while running:
        await asyncio.sleep(0)
        clock.tick(60)
        await asyncio.sleep(0)
        dt = clock.get_time() / 1000.0  # 経過時間（秒）

        # タイトルアニメ用時間
        if mode == "title":
            title_time += dt

        # フラッシュタイマー更新
        if flash_timer > 0:
            flash_timer -= dt
            if flash_timer < 0:
                flash_timer = 0

        # 問題文アニメーション時間更新
        if mode in ("select", "result"):
            q_anim_timer += dt

        # 背景
        if flash_timer > 0:
            # 正解直後は画面全体を明るめの色でフラッシュ
            screen.fill((255, 255, 200))
        else:
            if background is not None:
                screen.blit(background, (0, 0))
            else:
                screen.fill(WHITE)

        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # いつでも ESC で終了（ゲーム一覧に戻る想定）
                    running = False

                if event.key == K_SPACE:
                    if mode == "title":
                        # タイトル → ゲーム開始
                        mode = "select"
                        q_index = 0
                        score = 0
                        time_left = SELECT_TIME
                        select_is_maru = True
                        in_result = False
                        flash_timer = 0.0
                        q_anim_timer = 0.0
                        # ランダムに7問選ぶ
                        k = min(7, len(QUIZ_DATA))
                        quiz = random.sample(QUIZ_DATA, k)
                        # 最初の問題Surfaceを準備
                        build_question_surface(quiz[q_index][0])

                    elif mode == "select" and not in_result:
                        # ○と×を切り替える
                        select_is_maru = not select_is_maru

                    elif mode == "result":
                        # 次の問題へ進む
                        q_index += 1
                        if q_index >= len(quiz):
                            mode = "end"
                        else:
                            time_left = SELECT_TIME
                            select_is_maru = True
                            in_result = False
                            flash_timer = 0.0
                            q_anim_timer = 0.0
                            mode = "select"
                            build_question_surface(quiz[q_index][0])

                # 終了画面でのキー
                if mode == "end":
                    if event.key == K_r:
                        # Rキーでリトライ
                        mode = "select"
                        q_index = 0
                        score = 0
                        time_left = SELECT_TIME
                        select_is_maru = True
                        in_result = False
                        flash_timer = 0.0
                        q_anim_timer = 0.0
                        k = min(7, len(QUIZ_DATA))
                        quiz = random.sample(QUIZ_DATA, k)
                        build_question_surface(quiz[q_index][0])
                    # ESCは上で処理（終了）
        # -------------------------
        #  ロジック更新
        # -------------------------
        if mode == "select" and not in_result:
            time_left -= dt
            if time_left <= 0:
                # 時間切れ → 判定
                correct_answer = quiz[q_index][1]
                if select_is_maru == correct_answer:
                    score += 1
                    # 正解SE & フラッシュ
                    if correct_se is not None:
                        correct_se.play()
                    flash_timer = 0.2  # 0.2秒だけフラッシュ
                in_result = True
                mode = "result"

        # フォントいろいろ
        font_big   = pygame.font.Font(FONT_PATH, 240)  # ○×
        font_mid   = pygame.font.Font(FONT_PATH, 60)
        font_small = pygame.font.Font(FONT_PATH, 32)
        font_score = pygame.font.Font(FONT_PATH, 64)
        font_expl  = pygame.font.Font(FONT_PATH, 26)   # 解説用
        font_rank  = pygame.font.Font(FONT_PATH, 120)  # ランク表示用

        # -------------------------
        #  画面上部：のこり時間バー ＆ スコア
        # -------------------------
        if mode in ("select", "result", "end"):
            # のこり時間バー（画面上の方に大きく）
            bar_margin_x = 80
            bar_x = bar_margin_x
            bar_y = 20
            bar_w_full = SCREEN_WIDTH - bar_margin_x * 2  # ほぼ画面幅いっぱい
            bar_h = 50

            # 背景
            pygame.draw.rect(screen, (220, 220, 220), (bar_x, bar_y, bar_w_full, bar_h))

            # 残り時間に応じたバー
            if mode == "select":
                ratio = max(0.0, min(1.0, time_left / SELECT_TIME))
            else:
                ratio = 0.0
            bar_w = int(bar_w_full * ratio)
            bar_color = get_bar_color(ratio)
            pygame.draw.rect(screen, bar_color, (bar_x, bar_y, bar_w, bar_h))

            # スコア画像と数値（バーの下に配置）
            sx = bar_x + bar_w_full - 350
            sy = bar_y + bar_h + 20  # バーの下にずらす

            if score_img is not None:
                screen.blit(score_img, (sx, sy))
                score_x = sx + score_img.get_width() + 20
            else:
                score_label = font_small.render("Score", True, BLACK)
                screen.blit(score_label, (sx, sy))
                score_x = sx + score_label.get_width() + 20

            # 数字は黒色で大きく表示
            score_text = font_score.render(str(score), True, BLACK)
            screen.blit(score_text, (score_x, sy - 20))

        # -------------------------
        #  画面描画（モードごと）
        # -------------------------

        # タイトル画面（⑤：タイトルがふわっと揺れる・説明文点滅）
        if mode == "title":
            # タイトル揺れ（上下にふわふわ）
            title = font_mid.render("SwitchQuiz - ワンボタン○×クイズ", True, BLACK)
            offset_y = int(math.sin(title_time * 2.0) * 20)  # 上下 ±20px
            title_x = SCREEN_WIDTH//2 - title.get_width()//2
            title_y = SCREEN_HEIGHT//2 - 120 + offset_y
            screen.blit(title, (title_x, title_y))

            info1 = font_small.render("【操作方法】", True, BLACK)
            screen.blit(info1, (SCREEN_WIDTH//2 - info1.get_width()//2, SCREEN_HEIGHT//2))

            # 点滅する説明（Space でスタート）
            blink_on = (math.sin(title_time * 3.0) > 0)
            if blink_on:
                info2 = font_small.render("Space：スタート／○×切り替え（制限時間内）", True, GRAY)
                screen.blit(info2, (SCREEN_WIDTH//2 - info2.get_width()//2, SCREEN_HEIGHT//2 + 50))

            info3 = font_small.render("R：リトライ（終了画面）  /  ESC：ゲーム一覧に戻る（終了）", True, GRAY)
            screen.blit(info3, (SCREEN_WIDTH//2 - info3.get_width()//2, SCREEN_HEIGHT//2 + 90))

        # プレイ中・結果表示中
        elif mode in ("select", "result"):
            # -------------------------
            # ① 問題文：フェードイン＋拡大しながら表示
            # -------------------------
            if q_surface is not None and q_rect is not None:
                t = min(1.0, q_anim_timer / Q_ANIM_DURATION)
                # スケール 0.8 → 1.0
                scale = 0.8 + 0.2 * t
                new_w = int(q_surface.get_width() * scale)
                new_h = int(q_surface.get_height() * scale)
                if new_w <= 0: new_w = 1
                if new_h <= 0: new_h = 1
                scaled = pygame.transform.smoothscale(q_surface, (new_w, new_h))
                # フェードイン（α 0→255）
                alpha = int(255 * t)
                scaled.set_alpha(alpha)
                # ちょっとだけ下からせり上がるイメージ
                rect = scaled.get_rect()
                rect.centerx = SCREEN_WIDTH // 2
                base_top = 180
                rect.top = base_top + int((1.0 - t) * 30)
                screen.blit(scaled, rect)

            # ○×の表示（画面中央）
            symbol = "○" if select_is_maru else "×"
            color = BLUE if select_is_maru else RED
            s = font_big.render(symbol, True, color)
            s_x = SCREEN_WIDTH//2 - s.get_width()//2
            s_y = SCREEN_HEIGHT//2 - s.get_height()//2
            screen.blit(s, (s_x, s_y))

            # 正解／不正解の表示（○×の下）
            if mode == "result":
                correct_answer = quiz[q_index][1]
                is_correct = (select_is_maru == correct_answer)
                result_text = "正解！" if is_correct else "不正解..."
                result_color = GREEN if is_correct else RED
                r = pygame.font.Font(FONT_PATH, 80).render(result_text, True, result_color)
                r_x = SCREEN_WIDTH//2 - r.get_width()//2
                r_y = s_y + s.get_height() + 20
                screen.blit(r, (r_x, r_y))

            # 下のヒント
            if mode == "select":
                hint = font_small.render("Spaceキーで○×きりかえ（時間切れで自動判定）", True, GRAY)
                screen.blit(hint, (80, SCREEN_HEIGHT - 80))
            elif mode == "result":
                hint = font_small.render("Spaceキーで次の問題へ", True, GRAY)
                screen.blit(hint, (80, SCREEN_HEIGHT - 80))

            # 解説ボックス（画面右下）
            if mode == "result":
                q_text, q_ans, q_expl = quiz[q_index]
                box_w = 700
                box_h = 260
                margin = 40
                box_x = SCREEN_WIDTH - box_w - margin
                box_y = SCREEN_HEIGHT - box_h - margin
                rect = (box_x, box_y, box_w, box_h)
                draw_rounded_rect(screen, rect, (255, 250, 240), radius=15,
                                  border_color=(180, 160, 140), border_width=3)

                # 見出し
                title_ex = font_small.render("解説", True, BLACK)
                screen.blit(title_ex, (box_x + 20, box_y + 15))

                # 解説文を自動改行して表示
                expl_lines = wrap_text(q_expl, font_expl, box_w - 40)
                text_y = box_y + 60
                for line in expl_lines:
                    surf = font_expl.render(line, True, BLACK)
                    screen.blit(surf, (box_x + 20, text_y))
                    text_y += 32

        # 終了画面（⑥：ランク＆コメント表示）
        elif mode == "end":
            # 画面上部にまとめて配置するための基準Y座標
            base_y = 80  # お好みで 60〜120 の間で微調整してOK

            # 見出し
            end_text = font_mid.render("おつかれさま！", True, BLACK)
            screen.blit(
                end_text,
                (SCREEN_WIDTH // 2 - end_text.get_width() // 2, base_y)
            )

            # スコア表示
            total = len(quiz) if quiz else 7
            score_text_main = font_mid.render(f"スコア：{score} / {total}", True, BLACK)
            screen.blit(
                score_text_main,
                (SCREEN_WIDTH // 2 - score_text_main.get_width() // 2, base_y + 60)
            )

            # ランクとコメント（ここも上側にまとめる）
            rank, comment = get_rank_comment(score, total)
            rank_surf = font_rank.render(rank, True, (0, 0, 0))  # ランクは黒のまま
            screen.blit(
                rank_surf,
                (SCREEN_WIDTH // 2 - rank_surf.get_width() // 2, base_y + 340)
            )

            comment_surf = font_small.render(comment, True, BLACK)
            screen.blit(
                comment_surf,
                (SCREEN_WIDTH // 2 - comment_surf.get_width() // 2, base_y + 260)
            )

            # リトライ説明は少し下に（中央よりちょっと下あたり）
            restart_text = font_small.render(
                "Rキー：もう一度プレイ  /  ESCキー：ゲーム一覧に戻る（終了）",
                True, GRAY
            )
            screen.blit(
                restart_text,
                (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 150)
            )

        pygame.display.update()

    pygame.quit()
    return


asyncio.run(_web_main())