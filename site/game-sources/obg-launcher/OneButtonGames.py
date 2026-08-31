# coding: utf-8
import sys
import numpy as np #行列等を使うためのモジュール
import time #数秒待つ等を使うためのモジュール
import random #ランダムを使うためのモジュール
import sys  # sysモジュールはOS判定やプラットフォーム情報を取得するために使用します
import pygame  # ゲームライブラリPygameを読み込みます
from pygame.locals import *  # Pygameの定数を直接参照できるようにします
import os  # osモジュールは環境変数の設定に利用します
import math
from pathlib import Path
import glob
import traceback


APP_NAME = "OneButtonGames"
RESOURCE_ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))


def _handle_unexpected_error(exc_type, exc_value, exc_traceback):
    """GUI版でも起動エラーの原因を確認できるようにログを残す。"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    error_text = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    log_dir = Path(os.environ.get("LOCALAPPDATA", Path.home())) / APP_NAME
    log_path = log_dir / "error.log"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path.write_text(error_text, encoding="utf-8")
    except OSError:
        log_path = None

    if sys.platform == "win32":
        try:
            import ctypes
            detail = f"\n\nエラーログ: {log_path}" if log_path else ""
            ctypes.windll.user32.MessageBoxW(
                None,
                f"ゲームを起動できませんでした。{detail}",
                APP_NAME,
                0x10,
            )
        except Exception:
            pass

    sys.__excepthook__(exc_type, exc_value, exc_traceback)


def init_audio():
    """音声デバイスが利用できないPCでは無音ドライバーへ切り替える。"""
    try:
        pygame.mixer.init()
    except pygame.error:
        pygame.mixer.quit()
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        pygame.mixer.init()


def create_display(size):
    """1920x1080の座標系を維持したまま、実ディスプレイへ拡大縮小する。"""
    try:
        return pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.SCALED)
    except pygame.error:
        # SCALEDを利用できない古いドライバー向けのフォールバック。
        return pygame.display.set_mode(size, pygame.FULLSCREEN)


sys.excepthook = _handle_unexpected_error
os.chdir(RESOURCE_ROOT)




#初期化
pygame.init()
init_audio()
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
font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定したフォントファイルとサイズでフォントオブジェクトを生成します。

#ここから↑は基本何も変更する必要がない





#ウィンドウ作成
SCREEN_WIDTH  = 1920 #Xサイズ
SCREEN_HEIGHT = 1080 #Yサイズ
screen = create_display((SCREEN_WIDTH, SCREEN_HEIGHT)) #フルスクリーン
pygame.display.set_caption("pygame")

# 使いたい変数や画像などをここで定義
jouhou_1 = pygame.image.load("asset/jouhougame1.png").convert_alpha()
jouhou_2 = pygame.image.load("asset/jouhougame2.png").convert_alpha()
jouhou_3 = pygame.image.load("asset/jouhougame3.png").convert_alpha()
jouhou_4 = pygame.image.load("asset/jouhougame4.png").convert_alpha()

junsin_1 = pygame.image.load("asset/junsingame1.png").convert_alpha()
junsin_2 = pygame.image.load("asset/junsingame2.png").convert_alpha()
junsin_3 = pygame.image.load("asset/junsingame3.png").convert_alpha()
junsin_4 = pygame.image.load("asset/junsingame4.png").convert_alpha()
junsin_5 = pygame.image.load("asset/junsingame5.png").convert_alpha()
junsin_6 = pygame.image.load("asset/junsingame6.png").convert_alpha()

selectscene_image = pygame.image.load("asset/select1.png").convert_alpha()
selectscene_image1 = pygame.image.load("asset/select2.png").convert_alpha()
selectscene_image2 = pygame.image.load("asset/one bottun title.png").convert_alpha()
selectscene_sayuu = 2
selectscene_yajirusi = pygame.image.load("asset/left_yajirushi.png").convert_alpha()
selectscene_yajirusi1 = pygame.image.load("asset/right_yajirushi.png").convert_alpha()

image_kasoru=pygame.image.load("asset\kasoru.png").convert_alpha()
bgm = pygame.mixer.music.load("asset/BGM.mp3") 
click = pygame.mixer.Sound("asset/click.mp3") 
#パスを真似して間違わないようにしよう
pygame.mixer.music.play(-1)
clock = pygame.time.Clock() #フレームレート取得

high_score=0



def stop_all_audio():
    # mixerが未初期化なら何もしない（これでエラー回避）
    if not pygame.mixer.get_init():
        return

    # BGM停止
    pygame.mixer.music.stop()
    try:
        pygame.mixer.music.unload()
    except Exception:
        pass

    # 効果音など全チャンネル停止
    pygame.mixer.stop()
    click.set_volume(0.8)
    pygame.mixer.music.set_volume(1)  # 初期音量
    bgm = pygame.mixer.music.load("asset/BGM.mp3") 




# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  ゲーム一覧






def SwitchQuiz():
    # -----------------------------
    #  初期設定
    # -----------------------------
    pygame.init()

    # DPIまわり（Windows でボケないようにする）
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
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
    screen = create_display((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("SwitchQuiz")

    clock = pygame.time.Clock()

    # -----------------------------
    #  画像・音の読み込み
    # -----------------------------
    # 背景画像（なくても動く）
    bg_path = "作成されたゲーム\純真高等学校\SwitchQuiz\画像\背景.jpg"

    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
 

    # スコア表示用の画像
    score_img = None
    score_path = "作成されたゲーム\純真高等学校\SwitchQuiz\画像\score.png"
    score_img = pygame.image.load(score_path).convert_alpha()


    # サウンド：ミキサー初期化
    correct_se = None
    pygame.mixer.init()
    # 正解SE
    se_path ="作成されたゲーム\純真高等学校\SwitchQuiz\効果音・BGM\\twinkle.mp3"

    correct_se = pygame.mixer.Sound(se_path)
    # BGM
    
    bgm_path = "作成されたゲーム\純真高等学校\SwitchQuiz\効果音・BGM\\3.mp3"
    pygame.mixer.music.load(bgm_path)
    pygame.mixer.music.play(-1)  # ループ再生


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
    Q_ANIM_DURATION = 0.6
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
        nonlocal q_surface, q_rect

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
    while running:
        clock.tick(60)
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

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    

def チンチロバトル():
        
    # ==============================
    # 初期化
    # ==============================
    pygame.init()

    # 画面設定
    info = pygame.display.Info()
    W, H = info.current_w, info.current_h
    screen = create_display((W, H))
    pygame.display.set_caption("チンチロバトル")
    clock = pygame.time.Clock()

    # ==============================
    # フォント
    # ==============================
    try:
        font = pygame.font.Font("NotoSansJP-Regular.ttf", 48)
        desc_font = pygame.font.Font("NotoSansJP-Regular.ttf", 32)
        dice_font = pygame.font.Font("NotoSansJP-Regular.ttf", 72)
    except:
        font = pygame.font.SysFont(None, 48)
        desc_font = pygame.font.SysFont(None, 32)
        dice_font = pygame.font.SysFont(None, 72)

    # ==============================
    # パス
    # ==============================
    ASSET_DIR = os.path.join(os.path.dirname(__file__), "asset")
    IMG_DIR = "作成されたゲーム\純真高等学校\チンチロバトル\\asset\画像"
    SOUND_DIR = "作成されたゲーム\純真高等学校\チンチロバトル\\asset\効果音・BGM"

    # ==============================
    # 画像読み込み
    # ==============================
    DICE_SCALE = 6
    dice_imgs_raw = [
        pygame.image.load(os.path.join(IMG_DIR, f"dice{i}.png")).convert_alpha()
        for i in range(1, 7)
    ]
    dice_imgs = [
        pygame.transform.scale(img, (img.get_width() * DICE_SCALE, img.get_height() * DICE_SCALE))
        for img in dice_imgs_raw
    ]

    bg_img = pygame.image.load(os.path.join(IMG_DIR, "BG.png")).convert()
    bg_img = pygame.transform.scale(bg_img, (W, H))

    img_27 = pygame.image.load(os.path.join(IMG_DIR, "27.png")).convert_alpha()
    img_59 = pygame.image.load(os.path.join(IMG_DIR, "59.png")).convert_alpha()

    PLAYER_X, PLAYER_Y = 890, 875
    ENEMY_X, ENEMY_Y = 890, 100

    # ==============================
    # サウンド
    # ==============================
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(SOUND_DIR, "5.mp3"))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    roll_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "8.mp3"))

    # ==============================
    # ステージ設定
    # ==============================
    STAGES = [
        {"name": "ステージ1", "tries": 5, "ok": lambda r: sum(r) >= 10,
        "rule": "5回以内に、サイコロの合計が10以上を出せ"},
        {"name": "ステージ2", "tries": 5, "ok": lambda r: sum(r) >= 11,
        "rule": "5回以内に、サイコロの合計が11以上を出せ"},
        {"name": "ステージ3", "tries": 6, "ok": lambda r: sum(r) >= 12,
        "rule": "6回以内に、サイコロの合計が12以上を出せ"},
        {"name": "ステージ4", "tries": 7, "ok": lambda r: sum(r) >= 13,
        "rule": "7回以内に、サイコロの合計が13以上を出せ"},
        {"name": "ステージ5", "tries": 7, "ok": lambda r: sum(r) >= 14,
        "rule": "7回以内に、サイコロの合計が14以上を出せ"},
    ]

    TIME_LIMIT = 20

    # ==============================
    # 状態管理
    # ==============================
    MODE_TITLE = 0
    MODE_RULE = 1
    MODE_GAME = 2
    MODE_CLEAR = 3
    MODE_OVER = 4

    game_mode = MODE_TITLE
    stage_num = 0
    tries_left = STAGES[0]["tries"]
    current_dice = [1, 1, 1]

    start_time = 0
    game_clear = False
    game_over = False

    # キャラ演出
    px_off = py_off = 0
    ex_off = ey_off = 0

    anim_mode = "none"
    anim_timer = 0

    # サイコロアニメ
    dice_roll_anim = False
    dice_roll_timer = 0
    dice_roll_max = 60

    # 連打防止
    dice_roll_time_limit = 2
    last_roll_time = 0

    # ステージクリア演出
    stage_clear_effect = False
    stage_clear_timer = 0
    stage_clear_duration = 30

    # ==============================
    # 関数
    # ==============================
    def reset_offsets():
        nonlocal px_off, py_off, ex_off, ey_off
        px_off = py_off = 0
        ex_off = ey_off = 0

    def start_anim(mode):
        nonlocal anim_mode, anim_timer
        anim_mode = mode
        anim_timer = 19

    def update_anim():
        nonlocal anim_mode, anim_timer
        nonlocal px_off, py_off, ex_off, ey_off

        if anim_mode == "none":
            return

        if anim_timer <= 0:
            anim_mode = "none"
            reset_offsets()
            return

        if anim_mode == "attack":
            py_off = -12 if anim_timer > 9 else -6
            ey_off = 4 if anim_timer > 9 else 2
            ex_off = -2 if anim_timer % 2 == 0 else 2

        elif anim_mode == "miss":
            py_off = 6 if anim_timer > 6 else 2
            ex_off = ey_off = 0

        anim_timer -= 1

    def reset_all():
        nonlocal stage_num, tries_left, current_dice
        nonlocal game_clear, game_over
        nonlocal game_mode, start_time

        stage_num = 0
        tries_left = STAGES[0]["tries"]
        current_dice = [1, 1, 1]
        game_clear = False
        game_over = False
        reset_offsets()
        start_time = time.time()
        game_mode = MODE_GAME

    def start_stage_clear_effect():
        nonlocal stage_clear_effect, stage_clear_timer
        stage_clear_effect = True
        stage_clear_timer = stage_clear_duration

    def update_stage_clear_effect():
        nonlocal stage_clear_effect, stage_clear_timer
        if stage_clear_effect:
            if stage_clear_timer > 0:
                stage_clear_timer -= 1
            else:
                stage_clear_effect = False

    def roll():
        nonlocal dice_roll_anim, dice_roll_timer, last_roll_time
        if dice_roll_anim:
            return

        current_time = time.time()
        if current_time - last_roll_time < dice_roll_time_limit:
            return

        dice_roll_anim = True
        dice_roll_timer = dice_roll_max
        roll_sound.play()
        last_roll_time = current_time

    def update_dice_animation():
        nonlocal dice_roll_anim, dice_roll_timer
        nonlocal current_dice, tries_left, stage_num
        nonlocal game_over, game_clear, game_mode, start_time

        if not dice_roll_anim:
            return

        if dice_roll_timer > 0:
            current_dice = [random.randint(1, 6) for _ in range(3)]
            dice_roll_timer -= 1
            return

        dice_roll_anim = False
        current_dice = [random.randint(1, 6) for _ in range(3)]
        tries_left -= 1

        ok = STAGES[stage_num]["ok"](current_dice)

        if ok:
            start_anim("attack")
            start_stage_clear_effect()
        else:
            start_anim("miss")

        if ok:
            stage_num += 1
            if stage_num >= len(STAGES):
                game_clear = True
                game_mode = MODE_CLEAR
            else:
                tries_left = STAGES[stage_num]["tries"]
                start_time = time.time()
        else:
            if tries_left <= 0:
                game_over = True
                game_mode = MODE_OVER

    def draw_dice_total():
        total = sum(current_dice)

        label_text = dice_font.render("出目の合計：", True, (255, 255, 255))
        shadow_label_text = dice_font.render("出目の合計：", True, (0, 0, 0))
        screen.blit(shadow_label_text, (W - shadow_label_text.get_width() - 100, 25))
        screen.blit(label_text, (W - label_text.get_width() - 95, 20))

        shadow_text = dice_font.render(str(total), True, (0, 0, 0))
        screen.blit(shadow_text, (W - shadow_text.get_width() - 25, 25))

        total_text = dice_font.render(str(total), True, (255, 255, 255))
        screen.blit(total_text, (W - total_text.get_width() - 20, 20))

    # ==============================
    # 描画
    # ==============================
    def draw_title():
        screen.blit(bg_img, (0, 0))
        t1 = font.render("チンチロバトル", True, (0, 0, 0))
        t2 = desc_font.render("Enter：ゲーム開始", True, (0, 0, 0))
        t3 = desc_font.render("R：ルール説明", True, (0, 0, 0))
        t4 = desc_font.render("Esc：終了", True, (0, 0, 0))

        screen.blit(t1, (W // 2 - t1.get_width() // 2, 150))
        screen.blit(t2, (W // 2 - t2.get_width() // 2, 350))
        screen.blit(t3, (W // 2 - t3.get_width() // 2, 420))
        screen.blit(t4, (W // 2 - t4.get_width() // 2, 490))

    def draw_rule():
        screen.blit(bg_img, (0, 0))
        y = 150
        for st in STAGES:
            txt = desc_font.render(f"{st['name']}：{st['rule']}", True, (0, 0, 0))
            screen.blit(txt, (80, y))
            y += 70

        t1 = desc_font.render("Enter：ゲーム開始", True, (0, 0, 0))
        t2 = desc_font.render("B：タイトルに戻る", True, (0, 0, 0))
        screen.blit(t1, (80, H - 200))
        screen.blit(t2, (80, H - 130))

    def draw_game():
        screen.blit(bg_img, (0, 0))

        screen.blit(img_27, (PLAYER_X + px_off, PLAYER_Y + py_off))
        screen.blit(img_59, (ENEMY_X + ex_off, ENEMY_Y + ey_off))

        if anim_mode == "attack" and anim_timer > 0:
            screen.blit(font.render("!", True, (0, 0, 0)), (ENEMY_X + 120, ENEMY_Y - 20))
        if anim_mode == "miss" and anim_timer > 0:
            screen.blit(font.render("...", True, (0, 0, 0)), (PLAYER_X + 120, PLAYER_Y - 40))

        base_x = W // 2 - 350
        y = 600
        for i, v in enumerate(current_dice):
            screen.blit(dice_imgs[v - 1], (base_x + i * 250, y))

        name = STAGES[stage_num]["name"]
        rule = STAGES[stage_num]["rule"]
        screen.blit(font.render(name, True, (0, 0, 0)), (60, 40))
        screen.blit(desc_font.render(rule, True, (0, 0, 0)), (60, 110))

        screen.blit(font.render(f"残り回数: {tries_left}", True, (0, 0, 0)), (60, H - 200))

        remain = TIME_LIMIT - int(time.time() - start_time)
        screen.blit(font.render(f"残り時間: {remain} 秒", True, (0, 0, 0)), (60, H - 130))

        if stage_clear_effect:
            text = font.render("ステージクリア！", True, (255, 255, 255))
            shadow_text = font.render("ステージクリア！", True, (0, 0, 0))
            screen.blit(shadow_text, (W // 2 - shadow_text.get_width() // 2 + 2, H // 2 - 40 + 2))
            screen.blit(text, (W // 2 - text.get_width() // 2, H // 2 - 40))

        draw_dice_total()

        # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
        # ★ 追加：Spaceキー案内
        # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
        guide = desc_font.render("Spaceキーでサイコロを振る", True, (0, 0, 0))
        screen.blit(guide, (W // 2 - guide.get_width() // 2, H - 80))

    def draw_clear():
        screen.blit(bg_img, (0, 0))
        t1 = font.render("ゲームクリア！", True, (0, 0, 0))
        t2 = desc_font.render("Enter：タイトルへ", True, (0, 0, 0))
        t3 = desc_font.render("Esc：終了", True, (0, 0, 0))

        screen.blit(t1, (W // 2 - t1.get_width() // 2, 250))
        screen.blit(t2, (W // 2 - t2.get_width() // 2, 360))
        screen.blit(t3, (W // 2 - t3.get_width() // 2, 430))

    def draw_over():
        screen.blit(bg_img, (0, 0))
        t1 = font.render("ゲームオーバー", True, (0, 0, 0))
        t2 = desc_font.render("Enter：タイトルへ", True, (0, 0, 0))
        t3 = desc_font.render("Esc：終了", True, (0, 0, 0))

        screen.blit(t1, (W // 2 - t1.get_width() // 2, 250))
        screen.blit(t2, (W // 2 - t2.get_width() // 2, 360))
        screen.blit(t3, (W // 2 - t3.get_width() // 2, 430))

    # ==============================
    # メインループ
    # ==============================
    running=True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

                if game_mode == MODE_TITLE:
                    if event.key == K_RETURN:
                        reset_all()
                    elif event.key == K_r:
                        game_mode = MODE_RULE

                elif game_mode == MODE_RULE:
                    if event.key == K_RETURN:
                        reset_all()
                    elif event.key == K_b:
                        game_mode = MODE_TITLE

                elif game_mode == MODE_GAME:
                    if event.key == K_SPACE:
                        roll()

                elif game_mode == MODE_CLEAR:
                    if event.key == K_RETURN:
                        game_mode = MODE_TITLE

                elif game_mode == MODE_OVER:
                    if event.key == K_RETURN:
                        game_mode = MODE_TITLE

        if game_mode == MODE_GAME:
            if TIME_LIMIT - (time.time() - start_time) <= 0:
                game_mode = MODE_OVER

        update_dice_animation()
        update_anim()
        update_stage_clear_effect()

        if game_mode == MODE_TITLE:
            draw_title()
        elif game_mode == MODE_RULE:
            draw_rule()
        elif game_mode == MODE_GAME:
            draw_game()
        elif game_mode == MODE_CLEAR:
            draw_clear()
        elif game_mode == MODE_OVER:
            draw_over()

        pygame.display.update()
        clock.tick(60)



#-----------------------------------------------------------------------------------------------



def ロボットジャンプ():
    
    # --- 基本設定 ---
    W, H = 1920, 1080  # フルHD
    FONT_PATH = "NotoSansJP-Regular.ttf"
    FONT_SIZE = 48

    pygame.init()
    screen = create_display((W, H))
    pygame.display.set_caption("横スクロールジャンプゲーム")
    clock = pygame.time.Clock()

    # --- フォント設定 ---
    try:
        font = pygame.font.Font(FONT_PATH, FONT_SIZE)
    except IOError:
        font = pygame.font.SysFont(None, FONT_SIZE)

    # =========================================================
    # メニュー画面
    # =========================================================
    def show_menu():
        screen.fill((230, 240, 250))

        title_font = pygame.font.Font(FONT_PATH, 96)
        title = title_font.render("横スクロールジャンプゲーム", True, (10, 10, 40))
        screen.blit(title, ((W - title.get_width()) // 2, H // 4))

        guide_font = pygame.font.Font(FONT_PATH, 40)
        guide_lines = [
            "Enterキーでゲーム開始",
            "ESCキーで終了",
            "Spaceキー：ジャンプ（長押しでホバー）"
        ]
        for i, line in enumerate(guide_lines):
            guide_text = guide_font.render(line, True, (40, 40, 40))
            screen.blit(guide_text, ((W - guide_text.get_width()) // 2,
                                    H // 2 + i * 50))

        pygame.display.flip()

    # =========================================================
    # ゲームオーバー画面（白背景）
    # =========================================================
    def show_game_over(final_score):
        screen.fill((255, 255, 255))

        over_font = pygame.font.Font(FONT_PATH, 120)
        over_text = over_font.render("GAME OVER", True, (220, 50, 50))
        screen.blit(over_text, ((W - over_text.get_width()) // 2, H // 4))

        score_font = pygame.font.Font(FONT_PATH, 80)
        stext = score_font.render(f"Score: {final_score}", True, (40, 40, 40))
        screen.blit(stext, ((W - stext.get_width()) // 2, H // 2))

        menu_font = pygame.font.Font(FONT_PATH, 48)
        guide = menu_font.render("Rキー：リトライ ／ ESCキー：ゲーム一覧に戻る", True, (60, 60, 60))
        screen.blit(guide, ((W - guide.get_width()) // 2, H // 2 + 120))

        pygame.display.flip()

    # =========================================================
    # ゲーム本体
    # =========================================================
    def run_game():

        # ---------- 音 ----------
        jump_sound = None
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("作成されたゲーム\純真高等学校\ロボットジャンプ\\asset\効果音・BGM\\5.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.5)
            jump_sound = pygame.mixer.Sound("作成されたゲーム\純真高等学校\ロボットジャンプ\\asset\効果音・BGM\\10.mp3")
        except Exception as e:
            print("音ロード失敗:", e)

        # ---------- 画像 ----------
        try:
            bg1 = pygame.image.load("作成されたゲーム\純真高等学校\ロボットジャンプ\\asset\画像\\background.png").convert()
            bg2 = pygame.image.load("作成されたゲーム\純真高等学校\ロボットジャンプ\\asset\画像\\background.png").convert()
            bg1 = pygame.transform.scale(bg1, (W, H))
            bg2 = pygame.transform.scale(bg2, (W, H))

            walk_images = [
                pygame.image.load("作成されたゲーム\純真高等学校\ロボットジャンプ\\asset\画像\walk1.png").convert_alpha(),
                pygame.image.load("作成されたゲーム\純真高等学校\ロボットジャンプ\\asset\画像\walk2.png").convert_alpha()
            ]
            walk_images = [pygame.transform.scale(img, (140, 140)) for img in walk_images]

            jump_image = pygame.image.load("作成されたゲーム\純真高等学校\ロボットジャンプ\\asset\画像\jump.png").convert_alpha()
            jump_image = pygame.transform.scale(jump_image, (140, 140))

            # enemy1（歩く・赤い敵）
            enemy_raw = [
                pygame.image.load("作成されたゲーム\純真高等学校\ロボットジャンプ\\asset\画像\enemy1_walk1.png").convert_alpha(),
                pygame.image.load("作成されたゲーム\純真高等学校\ロボットジャンプ\\asset\画像\enemy1_walk2.png").convert_alpha()
            ]
            scale_factor = 0.9
            enemy_imgs = [
                pygame.transform.rotozoom(pygame.transform.flip(img, True, False), 0, scale_factor)
                for img in enemy_raw
            ]

            # enemy2（ジャンプして飛ぶ・羽ばたく敵）
            enemy2_raw = [
                pygame.image.load("作成されたゲーム\純真高等学校\ロボットジャンプ\\asset\画像\enemy2_up.png").convert_alpha(),
                pygame.image.load("作成されたゲーム\純真高等学校\ロボットジャンプ\\asset\画像\enemy2_down.png").convert_alpha()
            ]
            enemy2_imgs = [
                pygame.transform.rotozoom(pygame.transform.flip(img, True, False), 0, 1.0)
                for img in enemy2_raw
            ]
        except pygame.error as e:
            print("画像ロードエラー:", e)
            return 0

        # ---------- 初期化 ----------
        bg_x1 = 0
        bg_x2 = W
        scroll_speed = 7.0
        enemy_speed = 8.0

        enemy_frame = 0
        enemy_frame_timer = 0.0

        # プレイヤー
        player_rect = walk_images[0].get_rect()
        player_rect.midbottom = (W // 3, H - 50)

        vel_y = 0.0
        gravity = 1200.0          # ★ 重力
        jump_velocity = -650.0
        coyote_time = 0.20
        coyote_timer = 0.0
        on_ground = False

        # プレイヤーアニメ
        current_frame = 0
        player_anim_timer = 0.0
        player_anim_speed = 0.18

        # ホバー（浮遊）
        is_gliding = False
        GLIDE_GRAVITY = 20.0 
        GLIDE_TIME = 1.5 
        glide_timer = GLIDE_TIME
        can_air_action = False

        # 敵生成
        spacing = 900             # ★ 敵の間隔を広げる
        enemies = []
        for i in range(5):
            etype = random.choice(["walk", "fly"])
            imgs = enemy_imgs if etype == "walk" else enemy2_imgs
            r = imgs[0].get_rect()
            r.midbottom = (W + i * spacing, H - 50)
            enemies.append({
                "type": etype,
                "imgs": imgs,
                "rect": r,
                "vy": 0.0,
                "state": "run",
                "cleared": False  # スコア加算済みか
            })

        cleared_score = 0
        ground_rect = pygame.Rect(0, H - 50, W, 50)

        last_space = False

        # ============================================================
        # メインループ
        # ============================================================
        running = True
        while running:
            dt = clock.tick(60) / 1000.0
            keys = pygame.key.get_pressed()
            space_down = keys[K_SPACE]

            # ---- イベント処理 ----
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False  # ゲームを抜けてゲームオーバー画面へ

            # ---- スピード上昇（強め）----
            scroll_speed += 0.08 * dt
            enemy_speed += 0.10 * dt

            # ---- プレイヤー移動 ----
            move_speed = 300
            
            # ---- 背景 ----
            bg_x1 -= scroll_speed
            bg_x2 -= scroll_speed
            if bg_x1 <= -W:
                bg_x1 = bg_x2 + W
            if bg_x2 <= -W:
                bg_x2 = bg_x1 + W

            # ---- 地面接地 ----
            on_ground = player_rect.bottom >= ground_rect.top and vel_y >= 0
            if on_ground:
                coyote_timer = coyote_time
                player_rect.bottom = ground_rect.top
                vel_y = 0
                is_gliding = False
                can_air_action = True
                glide_timer = GLIDE_TIME
            else:
                coyote_timer = max(coyote_timer - dt, 0)

            # ---- ジャンプ ----
            if space_down and not last_space:
                if on_ground or coyote_timer > 0:
                    vel_y = jump_velocity
                    if jump_sound:
                        jump_sound.play()
                    can_air_action = True

            # ---- ホバー ----
            if (not on_ground) and space_down and can_air_action and glide_timer > 0:
                is_gliding = True
                glide_timer -= dt
            else:
                is_gliding = False
                if glide_timer <= 0:
                    can_air_action = False

            # ---- 重力 ----
            g = GLIDE_GRAVITY if is_gliding else gravity
            vel_y += g * dt
            player_rect.y += vel_y * dt

            if player_rect.bottom > ground_rect.top:
                player_rect.bottom = ground_rect.top
                vel_y = 0

            # ---- プレイヤーアニメ ----
            player_anim_timer += dt
            if player_anim_timer >= player_anim_speed:
                player_anim_timer = 0
                current_frame = (current_frame + 1) % len(walk_images)

            # ---- 敵処理 ----
            for e in enemies:
                e["rect"].x -= enemy_speed

                # ★ 飛び越え検知
                overlap_x = (e["rect"].left <= player_rect.centerx <= e["rect"].right)
                if overlap_x and (player_rect.bottom < e["rect"].top) and (not e["cleared"]):
                    cleared_score += 300 if e["type"] == "fly" else 100
                    e["cleared"] = True

                # enemy2 の大ジャンプ
                if e["type"] == "fly":
                    trigger_x = player_rect.centerx + 300
                    if e["state"] == "run" and e["rect"].left < trigger_x:
                        e["vy"] = -900
                        e["state"] = "jump"

                    if e["state"] == "jump":
                        e["rect"].y += e["vy"] * dt
                        e["vy"] += gravity * dt
                        if e["rect"].bottom > ground_rect.top:
                            e["rect"].bottom = ground_rect.top
                            e["state"] = "run"

                # 画面外 → 再出現
                if e["rect"].right < 0:
                    e["type"] = random.choice(["walk", "fly"])
                    e["imgs"] = enemy_imgs if e["type"] == "walk" else enemy2_imgs

                    rightmost = max(ee["rect"].right for ee in enemies)
                    spawn_x = max(W + 150, rightmost + spacing)

                    e["rect"] = e["imgs"][0].get_rect()
                    e["rect"].midbottom = (spawn_x, H - 50)
                    e["vy"] = 0.0
                    e["state"] = "run"
                    e["cleared"] = False

            # ---- 敵アニメ ----
            enemy_frame_timer += dt
            if enemy_frame_timer >= 0.18:
                enemy_frame_timer = 0
                enemy_frame = (enemy_frame + 1) % 2
                for e in enemies:
                    keep = e["rect"].midbottom
                    e["rect"] = e["imgs"][enemy_frame].get_rect()
                    e["rect"].midbottom = keep

            # ---- 当たり判定 ----
            player_box = player_rect.inflate(-20, -20)
            for e in enemies:
                enemy_box = e["rect"].inflate(-20, -20)
                if player_box.colliderect(enemy_box):
                    if pygame.mixer.get_init():
                        pygame.mixer.music.stop()
                    return cleared_score  # スコアを返してゲーム終了

            # ---- 描画 ----
            screen.blit(bg1, (bg_x1, 0))
            screen.blit(bg2, (bg_x2, 0))

            for e in enemies:
                screen.blit(e["imgs"][enemy_frame], e["rect"])

            pygame.draw.rect(screen, (100, 60, 60), ground_rect)

            if not on_ground:
                screen.blit(jump_image, player_rect)
            else:
                screen.blit(walk_images[current_frame], player_rect)

            # スコア表示
            score_text = font.render(f"Score: {cleared_score}", True, (20, 20, 20))
            screen.blit(score_text, (20, 20))

            pygame.display.flip()
            last_space = space_down

        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
        return cleared_score
    
       

    # =========================================================
    # メインループ（シーン管理）
    # =========================================================
    scene = "menu"
    running = True
    final_score = 0

    while running:
        if scene == "menu":
            show_menu()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key in (K_RETURN, K_KP_ENTER):
                        scene = "game"
                    elif event.key == K_ESCAPE:
                        running = False

        elif scene == "game":
            final_score = run_game()
            scene = "game_over"

        elif scene == "game_over":
            show_game_over(final_score)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_r:
                        scene = "game"      # タイトルを挟まず即リトライ
                    elif event.key == K_ESCAPE:
                        running = False


   


#--------------------------------------------------------------------------------------------------

def 音楽ゲーム():
    # coding: utf-8
    """
    _rhythm_like.py

    簡易的なリズムゲーム風デモです。
    """

    # OS設定
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    else:
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    W, H = 1920, 1080
    FONT_PATH = "NotoSansJP-Regular.ttf"
    FONT_SIZE = 30

    pygame.init()
    screen = create_display((W, H))
    pygame.display.set_caption("音楽ゲーム")

    try:
        font = pygame.font.Font(FONT_PATH, FONT_SIZE)
    except IOError:
        font = pygame.font.SysFont(None, FONT_SIZE)

    # 画像読み込み（ファイルパスは環境に合わせて）
    arrow_center = pygame.image.load("作成されたゲーム/純真高等学校/音楽ゲーム/asset/画像/3.png")
    arrow_left   = pygame.image.load("作成されたゲーム/純真高等学校/音楽ゲーム/asset/画像/4.png")
    arrow_right  = pygame.image.load("作成されたゲーム/純真高等学校/音楽ゲーム/asset/画像/5.png")
    arrow_imgs = [arrow_center, arrow_left, arrow_right]

    # 効果音・BGM
    test_se5 = pygame.mixer.Sound("作成されたゲーム/純真高等学校/音楽ゲーム/asset/効果音/5.mp3")
    test_se6 = pygame.mixer.Sound("作成されたゲーム/純真高等学校/音楽ゲーム/asset/効果音/6.mp3")
    test_se10 = pygame.mixer.Sound("作成されたゲーム/純真高等学校/音楽ゲーム/asset/効果音/10.mp3")
    test_se5.set_volume(0.8)
    test_se10.set_volume(0.6)

    test_se4 = pygame.mixer.Sound("作成されたゲーム/純真高等学校/音楽ゲーム/asset/効果音/4.mp3")
    test_se4.set_volume(1.0)

    # ゲーム状態
    notes = []
    decor_notes = []
    spawn_interval = 1500
    last_spawn = 0
    judge_line_y = H - 150

    CENTER_X = W // 2
    LEFT_X = W // 2 - 200
    RIGHT_X = W // 2 + 200

    perfect_window = 30
    ok_window = 50
    message = "中央列の矢印が判定ラインに来たらエンタキー"

    HP = 300
    point = 0
    スコア = point
    スコア = max(0, スコア + point)

    scene = "menu"

    clock = pygame.time.Clock()
    running = True
    elapsed_time = 0
    game_limit_ms = 60_000
    hyouzi_time = "0 秒"

    # ゲーム状態初期化
    def reset_game():
        nonlocal notes, decor_notes, elapsed_time, last_spawn, HP, point, message, hyouzi_time
        notes.clear()
        decor_notes.clear()
        elapsed_time = 0
        last_spawn = 0
        HP = 300
        point = 0
        message = "中央列の矢印が判定ラインに来たらエンターキー"
        hyouzi_time = "0 秒"

    while running:
        dt = clock.tick(60)
        elapsed_time += dt
        remain_ms = max(0, game_limit_ms - elapsed_time)
        hyouzi_time = f"残り {remain_ms // 1000:02d} 秒"

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            # キー押下イベント
            if event.type == KEYDOWN:

                # Eキーで強制終了 
                if event.key == K_e:
                    try:
                        test_se4.stop()
                    except:
                        pass
                    running=False

                # スペース：メニューからプレイ開始、またはクリア/オーバーから再挑戦
                if event.key == K_SPACE:
                    if scene == "menu":
                        scene = "play"
                        test_se4.stop()
                        test_se4.play(-1)
                    elif scene == "clear":
                        reset_game()
                        scene = "play"
                        test_se4.stop()
                        test_se4.play(-1)
                    elif scene == "over":
                        reset_game()
                        scene = "play"
                        test_se4.stop()
                        test_se4.play(-1)

                

                # Enter：プレイ中の判定
                elif event.key == K_RETURN and scene == "play":
                    result = None
                    for note in notes:
                        if not note.get('hit', False):
                            dist = abs(note['y'] - judge_line_y)
                            if dist <= ok_window:
                                note['hit'] = True
                                if dist <= perfect_window:
                                    result = "良"
                                    point = max(0, point + 10)
                                    test_se6.play()
                                else:
                                    result = "可"
                                    point = max(0, point + 5)
                                    HP = max(0, HP - 50)
                                    test_se5.play()
                                break
                    if result is None:
                        result = "不可"
                        HP = max(0, HP - 100)
                    message = result

        # シーンごとの処理
        if scene == "play":
            if remain_ms == 0:
                scene = "clear"
                message = "CLEAR!"

            if random.random() < 0.02:
                notes.append({'x': CENTER_X, 'y': -20, 'speed': 300, 'hit': False, 'img': arrow_center})
                last_spawn = elapsed_time
            if random.random() < 0.02:
                decor_notes.append({'x': LEFT_X, 'y': -20, 'speed': 300, 'img': arrow_left})
            if random.random() < 0.02:
                decor_notes.append({'x': RIGHT_X, 'y': -20, 'speed': 300, 'img': arrow_right})

            for note in notes[:]:
                note['y'] += note['speed'] * (dt / 1000.0)
                if note['y'] > judge_line_y + ok_window and not note.get('hit', False):
                    message = "不可"
                    HP = max(0, HP - 50)
                    try:
                        notes.remove(note)
                    except ValueError:
                        pass
                elif note['y'] > H + 40:
                    if note in notes:
                        notes.remove(note)

            for dnote in decor_notes[:]:
                dnote['y'] += dnote['speed'] * (dt / 1000.0)
                if dnote['y'] > H + 40:
                    try:
                        decor_notes.remove(dnote)
                    except ValueError:
                        pass

            for dnote in decor_notes:
                dist = abs(dnote['y'] - judge_line_y)
                if dist <= 20:
                    test_se10.play()

            if HP <= 0:
                scene = "over"
                message = "GAME OVER"

            screen.fill((255, 255, 255))
            pygame.draw.line(screen, (200, 200, 200), (0, judge_line_y), (W, judge_line_y), 4)

            for note in notes:
                img = note['img']
                rect = img.get_rect(center=(note['x'], note['y']))
                screen.blit(img, rect.topleft)

            for dnote in decor_notes:
                img = dnote['img']
                rect = img.get_rect(center=(dnote['x'], dnote['y']))
                screen.blit(img, rect.topleft)

            msg_surface1 = font.render(str(message), True, (0, 0, 0))
            msg_surface2 = font.render(str(hyouzi_time), True, (0, 0, 0))
            msg_surface3 = font.render(str(point), True, (0, 0, 0))
            msg_surface_hp = font.render(f"HP: {HP}", True, (0, 0, 0))

            screen.blit(msg_surface1, ((W - msg_surface1.get_width()) // 2, judge_line_y + 20))
            screen.blit(msg_surface2, (20, H - 80))
            screen.blit(msg_surface_hp, (20, H - 40))
            screen.blit(msg_surface3, (1000, 50))

            guide = font.render("中央列の矢印が判定ラインに来たらエンターキーを押してください", True, (0, 0, 0))
            screen.blit(guide, (20, 20))
            guide2 = font.render("Eキーでゲームを終了する", True, (0, 0, 0))
            screen.blit(guide2, (20, 70))
            pygame.display.flip()
            continue

        if scene == "menu":
            screen.fill((255, 255, 255))
            title  = font.render("GAME START!", True, (0, 0, 0))
            guide2 = font.render("スペースキーでスタート", True, (0, 0, 0))
            guide3 = font.render("中央列の矢印が判定ラインに来たらエンターキーを押してください", True, (0, 0, 0))
            guide5 = font.render("Eキーでゲームを終了する", True, (0, 0, 0))
            screen.blit(title, ((W - title.get_width()) // 2, H // 2 - 40))
            screen.blit(title, ((W - title.get_width()) // 2, H // 2 - 40))
            screen.blit(guide2, ((W - guide2.get_width()) // 2, H // 2 + 10))
            screen.blit(guide3, (500, H // 2 + 60))
            
            screen.blit(guide5, (750, H // 2 + 130))
            pygame.display.flip()
            continue

        if scene == "over":
            test_se4.stop()
            screen.fill((255, 255, 255))
            title = font.render("GAME OVER", True, (0, 0, 0))
            guide2 = font.render("スペースキーで再チャレンジ", True, (0, 0, 0))
            guide5 = font.render("Eキーでゲームを終了する", True, (0, 0, 0))
            screen.blit(title, ((W - title.get_width()) // 2, H // 2 - 40))
            screen.blit(guide2, ((W - guide2.get_width()) // 2, H // 2 + 10))
            screen.blit(guide5, ((W - guide2.get_width()) // 2, H // 2 + 50))
            pygame.display.flip()
            continue

        if scene == "clear":
            test_se4.stop()
            screen.fill((255, 255, 255))
            title = font.render("GAME CLEAR!", True, (0, 0, 0))
            guide2 = font.render("スペースキーでタイトルへ", True, (0, 0, 0))
            guide5 = font.render("Eキーでゲームを終了する", True, (0, 0, 0))
            screen.blit(title, ((W - title.get_width()) // 2, H // 2 - 40))
            screen.blit(guide2, ((W - guide2.get_width()) // 2, H // 2 + 10))
            screen.blit(guide5, ((W - guide2.get_width()) // 2, H // 2 + 50))
            pygame.display.flip()
            continue

        pygame.display.flip()

    

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def 時の管理者():
    
    

    # ============================================
    # 基本設定 (Basic Settings)
    # ============================================
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080
    FPS = 60
    GAME_TITLE = "時の管理者"

    # ============================================
    # 色定義 (Color Definitions)
    # ============================================
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GRAY = (128, 128, 128)
    LIGHT_BLUE = (173, 216, 230)
    PURPLE = (147, 112, 219)
    ORANGE = (255, 165, 0)
    DARK_GRAY = (50, 50, 50)

    from pathlib import Path

    # ============================================
    # 実行ファイル（この .py）の場所を基準にした相対パス
    # ============================================
    BASE_DIR = Path(__file__).resolve().parent

    GAME_ROOT = BASE_DIR / "作成されたゲーム" / "純真高等学校" / "時の管理者"
    ASSET_DIR = GAME_ROOT / "asset"
    IMG_DIR   = ASSET_DIR / "画像"
    SND_DIR   = ASSET_DIR / "効果音・BGM"


    # ============================================
    # フォント（.py と同じフォルダの日本語フォントを使う）
    # ============================================
    JP_FONT_TTF = BASE_DIR / "NotoSansJP-Regular.ttf"
    JP_FONT_OTF = BASE_DIR / "NotoSansJP-Regular.otf"
    JP_FONT_PATH = JP_FONT_TTF if JP_FONT_TTF.exists() else JP_FONT_OTF

    # ============================================
    # 画像 / 音ファイルパス定義（配布可能な相対パス）
    # ============================================
    PLAYER_IMG_PATH = str(IMG_DIR / "130.png")
    BOSS_IMG_PATH   = str(IMG_DIR / "80.png")
    ITEM_IMG_PATH   = str(IMG_DIR / "82.png")

    ENTER_SFX_PATH  = str(SND_DIR / "9.mp3")
    BOSS_SFX_PATH   = str(SND_DIR / "1.mp3")

    # BGMは「効果音・BGM」フォルダに入っている前提に統一します
    BGM_PATH        = str(SND_DIR / "bgm_loop.ogg")   # もしファイル名が違うならここだけ修正


    # ============================================
    # ゲーム状態 (Game States)
    # ============================================
    TITLE_SCREEN = "TITLE_SCREEN"
    COLLECT_PHASE = "COLLECT_PHASE"
    BOSS_PHASE = "BOSS_PHASE"
    GAME_CLEAR = "GAME_CLEAR"
    GAME_OVER = "GAME_OVER"
    GAME_CLEAR_ANIM = "GAME_CLEAR_ANIM"
    SCORE_SCREEN = "SCORE_SCREEN"

    # ============================================
    # プレイヤー設定 (Player Settings)
    # ============================================
    PLAYER_SIZE = 64
    PLAYER_SPEED = 6
    JUMP_FORCE = -18
    GRAVITY = 1.0
    GROUND_Y = WINDOW_HEIGHT - 80

    # ============================================
    # 入力判定閾値 (Input Thresholds)
    # ============================================
    SHORT_PRESS_THRESHOLD = 0.15
    LONG_PRESS_THRESHOLD = 0.5
    DOUBLE_TAP_THRESHOLD = 0.3

    # ============================================
    # タイマー設定 (Timer Settings)
    # ============================================
    COLLECT_PHASE_TIME = 30

    # ============================================
    # 雷設定 (Lightning Settings)
    # ============================================
    LIGHTNING_INTERVAL = 5.0
    LIGHTNING_CHARGE = 1.0
    LIGHTNING_DURATION = 0.35

    # 雷のバリエーション（色とダメージ倍率）
    LIGHTNING_VARIANTS = [
        {"name": "弱", "color": LIGHT_BLUE, "factor": 1.0},
        {"name": "中", "color": YELLOW, "factor": 1.4},
        {"name": "強", "color": PURPLE, "factor": 1.8},
        {"name": "極", "color": ORANGE, "factor": 2.4},
    ]


    class ImageLoader:
        """画像ファイルの読み込みとフォールバック管理（強化版）"""

        IMAGE_EXTS = [".png", ".jpg", ".jpeg", ".bmp", ".gif"]

        def __init__(self):
            self.images = {}
            self.use_fallback = {}
            self.paths = {}

        def _find_image_in_dir(self, dirpath):
            p = Path(dirpath)
            if not p.exists() or not p.is_dir():
                return None
            for ext in self.IMAGE_EXTS:
                for f in p.glob(f"*{ext}"):
                    return str(f)
            files = list(p.iterdir())
            return str(files[0]) if files else None

        def _try_variants(self, raw_path):
            """パスの空白や同等のファイル名を緩和して探す"""
            path = os.path.normpath(raw_path.strip())
            p = Path(path)
            if p.exists():
                return str(p)

            if str(raw_path).endswith(os.sep) or (p.parent.exists() and p.name == ""):
                found = self._find_image_in_dir(str(p))
                if found:
                    return found

            n = " ".join(raw_path.split())
            parent = p.parent if p.parent.exists() else Path(".")
            base = p.name
            base_no_space = base.replace(" ", "")
            for f in parent.iterdir() if parent.exists() else []:
                fname = f.name
                if fname.replace(" ", "") == base_no_space:
                    return str(f)
            glob_try = glob.glob(raw_path + "*")
            for g in glob_try:
                if any(g.lower().endswith(ext) for ext in self.IMAGE_EXTS):
                    return g
            return None

        def load_image(self, name, path, fallback_size=None):
            """画像を読み込み、失敗時はフォールバックフラグを設定"""
            self.paths[name] = path
            found = None
            try:
                if path:
                    cand = self._try_variants(path)
                    if cand:
                        found = cand
                    else:
                        cand2 = self._find_image_in_dir(path)
                        if cand2:
                            found = cand2

                if found and Path(found).exists():
                    img = pygame.image.load(str(found)).convert_alpha()
                    if fallback_size:
                        img = pygame.transform.smoothscale(img, (fallback_size[0], fallback_size[1]))
                    self.images[name] = img
                    self.use_fallback[name] = False
                    self.paths[name] = str(found)
                    return
                raise FileNotFoundError(f"Image not found (after variants): {path}")
            except Exception as e:
                print(f"画像読み込み失敗 ({path}): {e} - 図形描画に切り替えます")
                self.images[name] = None
                self.use_fallback[name] = True

        def should_use_fallback(self, name):
            return self.use_fallback.get(name, True)

        def get_image(self, name):
            return self.images.get(name)


    class MagicProjectile:
        """プレイヤーの魔法弾（単発、ボスに命中するとダメージ）"""

        def __init__(self, x, y, target_x, target_y, speed=9, damage=1, color=(100, 200, 255)):
            self.x = x
            self.y = y
            dx = target_x - x
            dy = target_y - y
            dist = max(math.hypot(dx, dy), 0.001)
            self.vx = dx / dist * speed
            self.vy = dy / dist * speed
            self.radius = 14
            self.active = True
            self.damage = damage
            self.color = color
            self.spawn_time = time.time()
            self.glow_radius = self.radius * 2
            self.rotation = random.uniform(0, math.pi * 2)

        def update(self):
            self.x += self.vx
            self.y += self.vy
            if self.x < -200 or self.x > WINDOW_WIDTH + 200 or self.y < -200 or self.y > WINDOW_HEIGHT + 200:
                self.active = False
            if time.time() - self.spawn_time > 6.0:
                self.active = False

        def draw(self, screen):
            glow_r = int(self.glow_radius)
            surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
            for i in range(4, 0, -1):
                a = int(40 * (1.0 - i * 0.12))
                pygame.draw.circle(surf, (*self.color, a), (glow_r, glow_r), int(glow_r * (i / 4.0)))
            screen.blit(surf, (int(self.x - glow_r), int(self.y - glow_r)), special_flags=pygame.BLEND_ADD)

            for i in range(6):
                ang = self.rotation + i * (math.pi * 2 / 6)
                lx = int(self.x + math.cos(ang) * (self.radius + 8))
                ly = int(self.y + math.sin(ang) * (self.radius + 8))
                pygame.draw.line(screen, WHITE, (int(self.x), int(self.y)), (lx, ly), 2)

            for i in range(4):
                talpha = int(80 * (1.0 - i * 0.22))
                tx = int(self.x - self.vx * i * 0.6)
                ty = int(self.y - self.vy * i * 0.6)
                rr = max(2, int(self.radius * (1.0 - i * 0.18)))
                s = pygame.Surface((rr * 2, rr * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*self.color, talpha), (rr, rr), rr)
                screen.blit(s, (tx - rr, ty - rr), special_flags=pygame.BLEND_PREMULTIPLIED)

            s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, 255), (self.radius, self.radius), self.radius)
            pygame.draw.circle(s, WHITE, (self.radius, self.radius), self.radius, 2)
            screen.blit(s, (int(self.x - self.radius), int(self.y - self.radius)))

        def get_rect(self):
            return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)


    class Orb:
        """Tama wo Tobasu の小弾（複数）"""

        def __init__(self, x, y, target_x, target_y, speed=7, damage=1, color=(200, 160, 255)):
            self.x = x
            self.y = y
            dx = target_x - x + random.uniform(-80, 80)
            dy = target_y - y + random.uniform(-40, 40)
            dist = max(math.hypot(dx, dy), 0.001)
            self.vx = dx / dist * speed
            self.vy = dy / dist * speed
            self.radius = 10
            self.active = True
            self.damage = damage
            self.color = color
            self.spawn_time = time.time()
            self.rotation = random.uniform(0, math.pi * 2)

        def update(self):
            self.x += self.vx
            self.y += self.vy
            if self.x < -200 or self.x > WINDOW_WIDTH + 200 or self.y < -200 or self.y > WINDOW_HEIGHT + 200:
                self.active = False
            if time.time() - self.spawn_time > 6.0:
                self.active = False

        def draw(self, screen):
            for i in range(3):
                rr = int(self.radius * (1.0 + i * 0.18))
                a = int(60 * (1.0 - i * 0.3))
                surf = pygame.Surface((rr * 2, rr * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, (*self.color, a), (rr, rr), rr)
                screen.blit(surf, (int(self.x - rr), int(self.y - rr)), special_flags=pygame.BLEND_PREMULTIPLIED)
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2)

        def get_rect(self):
            return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)


    class Fireball:
        """ボスの炎攻撃（ファイアボール）"""

        def __init__(self, x, y, target_x, target_y, speed=6):
            self.x = x
            self.y = y
            dx = target_x - x
            dy = target_y - y
            dist = max(math.hypot(dx, dy), 0.01)
            self.vx = dx / dist * speed
            self.vy = dy / dist * speed
            self.radius = 10
            self.active = True
            self.spawn_time = time.time()

        def update(self):
            self.x += self.vx
            self.y += self.vy
            if self.x < -50 or self.x > WINDOW_WIDTH + 50 or self.y < -50 or self.y > WINDOW_HEIGHT + 50:
                self.active = False
            if time.time() - self.spawn_time > 6.0:
                self.active = False

        def draw(self, screen):
            g = pygame.Surface((self.radius * 6, self.radius * 6), pygame.SRCALPHA)
            gg = int(self.radius * 2.5)
            pygame.draw.circle(g, (255, 140, 20, 140), (g.get_width() // 2, g.get_height() // 2), gg)
            screen.blit(g, (int(self.x - g.get_width() // 2), int(self.y - g.get_height() // 2)), special_flags=pygame.BLEND_ADD)
            pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, (255, 120, 0), (int(self.x), int(self.y)), self.radius, 2)
            for i in range(3):
                tx = int(self.x - self.vx * (i + 1) * 0.4)
                ty = int(self.y - self.vy * (i + 1) * 0.4)
                ta = int(90 * (1.0 - i * 0.33))
                rr = max(2, int(self.radius * (0.8 - i * 0.2)))
                surf = pygame.Surface((rr * 2, rr * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, (255, 150, 40, ta), (rr, rr), rr)
                screen.blit(surf, (tx - rr, ty - rr), special_flags=pygame.BLEND_PREMULTIPLIED)

        def get_rect(self):
            return pygame.Rect(int(self.x) - self.radius, int(self.y) - self.radius, self.radius * 2, self.radius * 2)


    class Particle:
        """単純な粒子（アイテム取得や被弾エフェクト用）"""

        def __init__(self, x, y, color, life=0.6):
            self.x = x
            self.y = y
            self.vx = random.uniform(-2.5, 2.5)
            self.vy = random.uniform(-3.5, -0.5)
            self.color = color
            self.life = life
            self.created = time.time()
            self.size = random.randint(2, 5)

        def update(self):
            self.vy += 0.12
            self.x += self.vx
            self.y += self.vy

        def draw(self, screen):
            age = time.time() - self.created
            alpha = max(0, 255 - int((age / self.life) * 255))
            surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color[:3], alpha), (self.size, self.size), self.size)
            screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))

        def is_dead(self):
            return (time.time() - self.created) > self.life


    class Player:
        """プレイヤークラス"""

        def __init__(self, image_loader):
            self.x = 100
            self.y = GROUND_Y - PLAYER_SIZE
            self.vel_x = 0
            self.vel_y = 0
            self.is_grounded = True
            self.image_loader = image_loader
            self.collected_items = 0
            self.facing_right = True
            self.max_hp = 5
            self.hp = self.max_hp
            self.dead = False
            self.collapse_start = None
            self.attack_power = 1
            self.recalc_stats()

        def move_right(self):
            self.vel_x = PLAYER_SPEED
            self.facing_right = True

        def move_left(self):
            self.vel_x = -int(PLAYER_SPEED * 1.6)
            self.facing_right = False

        def stop(self):
            self.vel_x *= 0.6
            if abs(self.vel_x) < 0.3:
                self.vel_x = 0

        def jump(self):
            if self.is_grounded and not self.dead:
                self.vel_y = JUMP_FORCE
                self.is_grounded = False

        def update(self):
            if self.dead:
                self.vel_y += GRAVITY
                self.x += self.vel_x * 0.3
                self.y += self.vel_y
                if self.collapse_start and time.time() - self.collapse_start > 2.5:
                    self.vel_x = 0
                return

            self.vel_y += GRAVITY
            self.x += self.vel_x
            self.y += self.vel_y

            self.vel_x *= 0.95

            if self.x < 0:
                self.x = 0
                self.vel_x = 0
            if self.x > WINDOW_WIDTH - PLAYER_SIZE:
                self.x = WINDOW_WIDTH - PLAYER_SIZE
                self.vel_x = 0

            if self.y >= GROUND_Y - PLAYER_SIZE:
                self.y = GROUND_Y - PLAYER_SIZE
                self.vel_y = 0
                self.is_grounded = True

        def take_damage(self, amount):
            if self.dead:
                return
            self.hp = max(0, self.hp - amount)
            if self.hp <= 0:
                self.dead = True
                self.collapse_start = time.time()

        def draw(self, screen):
            if self.image_loader.should_use_fallback("player"):
                color = DARK_GRAY if self.dead else GREEN
                pygame.draw.rect(screen, color, (int(self.x), int(self.y), PLAYER_SIZE, PLAYER_SIZE), border_radius=6)
            else:
                img = self.image_loader.get_image("player")
                if img:
                    img_to_draw = img
                    if self.dead:
                        img_to_draw = img.copy()
                        arr = pygame.Surface(img_to_draw.get_size(), pygame.SRCALPHA)
                        arr.fill((0, 0, 0, 120))
                        img_to_draw.blit(arr, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
                    screen.blit(img_to_draw, (int(self.x), int(self.y)))

        def recalc_stats(self):
            """Collect に応じて最大HPと攻撃力を再計算する"""
            prev_max = getattr(self, "max_hp", 5)
            self.max_hp = 5 + (self.collected_items // 5)
            self.attack_power = 1 + (self.collected_items // 3)
            if self.max_hp > prev_max:
                self.hp = min(self.max_hp, self.hp + (self.max_hp - prev_max))

        def get_rect(self):
            return pygame.Rect(int(self.x), int(self.y), PLAYER_SIZE, PLAYER_SIZE)


    class Item:
        """アイテム（記憶の断片）クラス - 空から降るように初期化可能"""

        def __init__(self, x, y, image_loader):
            self.x = x
            self.y = y
            self.radius = 7
            self.image_loader = image_loader
            self.collected = False
            self.vy = 0.0
            self.dropped = True if y >= GROUND_Y - 40 else False

        def update(self):
            if self.collected:
                return
            if not self.dropped:
                self.vy += 0.25
                self.y += self.vy
                if self.y >= GROUND_Y - 16:
                    self.y = GROUND_Y - 16
                    self.vy = 0.0
                    self.dropped = True

        def draw(self, screen):
            if not self.collected:
                if self.image_loader.should_use_fallback("item"):
                    pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
                    pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.radius, 2)
                else:
                    img = self.image_loader.get_image("item")
                    if img:
                        w, h = img.get_size()
                        screen.blit(img, (int(self.x - w / 2), int(self.y - h / 2)))

        def get_rect(self):
            return pygame.Rect(int(self.x) - self.radius, int(self.y) - self.radius, self.radius * 2, self.radius * 2)


    class Boss:
        """Boss (Administrator) class"""

        def __init__(self, image_loader):
            self.x = WINDOW_WIDTH // 2
            self.y = WINDOW_HEIGHT // 2 - 50
            self.radius = 54
            self.hp = 30
            self.max_hp = 30
            self.image_loader = image_loader
            self.vel_x = random.choice([-2, 2])
            self.vel_y = random.choice([-1, 1])
            self.move_timer = time.time()
            self.direction_change_interval = random.uniform(1.0, 3.0)
            self.last_fire_time = time.time()
            self.fire_interval = random.uniform(2.0, 4.0)

        def update(self):
            current_time = time.time()
            if current_time - self.move_timer > self.direction_change_interval:
                self.vel_x = random.uniform(-3, 3)
                self.vel_y = random.uniform(-2, 2)
                self.direction_change_interval = random.uniform(1.0, 3.0)
                self.move_timer = current_time

            self.x += self.vel_x
            self.y += self.vel_y

            if self.x < self.radius + 100:
                self.x = self.radius + 100
                self.vel_x = abs(self.vel_x)
            if self.x > WINDOW_WIDTH - self.radius:
                self.x = WINDOW_WIDTH - self.radius
                self.vel_x = -abs(self.vel_x)
            if self.y < self.radius + 50:
                self.y = self.radius + 50
                self.vel_y = abs(self.vel_y)
            if self.y > GROUND_Y - self.radius - 50:
                self.y = GROUND_Y - self.radius - 50
                self.vel_y = -abs(self.vel_y)

        def draw(self, screen):
            if self.image_loader.should_use_fallback("boss"):
                pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
                pygame.draw.circle(screen, (200, 0, 0), (int(self.x), int(self.y)), self.radius, 4)
            else:
                img = self.image_loader.get_image("boss")
                if img:
                    w, h = img.get_size()
                    screen.blit(img, (int(self.x - w // 2), int(self.y - h // 2)))


    class Lightning:
        """雷エフェクトクラス"""

        def __init__(self, x):
            self.x = x
            self.variant = random.choice(LIGHTNING_VARIANTS)
            self.color = self.variant["color"]
            self.damage_factor = self.variant["factor"]
            self.name = self.variant["name"]
            self.active = True
            self.start_time = time.time()
            self.charge_duration = random.uniform(0.6, 1.4)
            self.phase = "charge"
            self.points = self._generate_zigzag()
            self.strike_point = self.points[-1] if self.points else (self.x, WINDOW_HEIGHT)
            self.intensity = random.uniform(1.0, 2.2)
            self.bolt_start = None

        def _generate_zigzag(self):
            points = [(self.x, 0)]
            y = 0
            while y < WINDOW_HEIGHT:
                y += random.randint(30, 120)
                x_offset = random.randint(-120, 120)
                points.append((self.x + x_offset, min(y, WINDOW_HEIGHT)))
            return points

        def update(self):
            now = time.time()
            if self.phase == "charge":
                if now - self.start_time > self.charge_duration:
                    self.phase = "bolt"
                    self.bolt_start = now
            elif self.phase == "bolt":
                if now - (self.bolt_start or now) > LIGHTNING_DURATION:
                    self.strike_point = self.points[-1] if self.points else (self.x, WINDOW_HEIGHT)
                    self.active = False
                    self.intensity = min(3.0, self.intensity * 1.2)

        def draw(self, screen):
            if self.phase == "charge":
                charge_t = (time.time() - self.start_time) / max(0.001, self.charge_duration)
                orb_y = max(60, int(min(WINDOW_HEIGHT * 0.4, 60 + charge_t * 220)))
                orb_radius = int(12 + charge_t * 28 * self.intensity)
                surf = pygame.Surface((orb_radius * 2, orb_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, (*self.color, int(40 + 200 * charge_t)), (orb_radius, orb_radius), orb_radius)
                screen.blit(surf, (int(self.x - orb_radius), int(orb_y - orb_radius)))
                for _ in range(6):
                    if random.random() < charge_t:
                        sx = int(self.x + random.randint(-40, 40))
                        sy = int(orb_y + random.randint(-20, 20))
                        pygame.draw.circle(screen, WHITE, (sx, sy), 2)
            elif self.phase == "bolt" and len(self.points) > 1:
                for i in range(len(self.points) - 1):
                    p1 = self.points[i]
                    p2 = self.points[i + 1]
                    thickness = random.choice([5, 6, 8])
                    pygame.draw.line(screen, self.color, p1, p2, thickness)
                    if random.random() < 0.5:
                        sx = (p1[0] + p2[0]) // 2 + random.randint(-20, 20)
                        sy = (p1[1] + p2[1]) // 2 + random.randint(-20, 20)
                        pygame.draw.circle(screen, WHITE, (sx, sy), 4)
                    if random.random() < 0.35:
                        bx = (p1[0] + p2[0]) // 2 + random.randint(-50, 50)
                        by = (p1[1] + p2[1]) // 2 + random.randint(-50, 50)
                        pygame.draw.line(screen, self.color, (bx, by), (bx + random.randint(-30, 30), by + random.randint(10, 90)), 2)
                strike_x = int(self.points[-1][0]) if self.points else int(self.x)
                prog = min(1.0, max(0.0, (time.time() - (self.bolt_start or time.time())) / max(0.001, LIGHTNING_DURATION)))
                glow_alpha = int(180 * (1.0 - prog))
                glow_r = int(120 * (0.8 + self.intensity * 0.2))
                glow = pygame.Surface((glow_r * 2, 80), pygame.SRCALPHA)
                gc = tuple(min(255, int(self.color[i] * 0.6 + 200 * 0.4)) for i in range(3))
                pygame.draw.ellipse(glow, (*gc, glow_alpha), (0, 0, glow_r * 2, 80))
                screen.blit(glow, (strike_x - glow_r, GROUND_Y - 40), special_flags=pygame.BLEND_ADD)


    class BurningZone:
        """燃えるゾーン（雷が落ちた後、またはボスの破壊で発生）"""

        def __init__(self, x, y, width=160, duration=8.0):
            self.x = max(0, min(WINDOW_WIDTH - width, int(x - width // 2)))
            self.y = y
            self.width = width
            self.duration = duration
            self.start = time.time()
            self.active = True

        def update(self):
            if time.time() - self.start > self.duration:
                self.active = False

        def draw(self, surface):
            age = (time.time() - self.start) / self.duration
            alpha = int(max(0, 180 * (1.0 - age)))
            surf = pygame.Surface((self.width, WINDOW_HEIGHT - self.y), pygame.SRCALPHA)
            color = (255, 100, 20, alpha)
            surf.fill(color)
            surface.blit(surf, (self.x, self.y))


    class Bomb:
        """落下する爆弾。着地で爆発し燃焼ゾーンを作る"""

        def __init__(self, x):
            self.x = x
            self.y = -40
            self.vy = random.uniform(8.0, 14.0)
            self.active = True
            self.exploded = False
            self.spawn = time.time()
            self.intensity = random.uniform(0.9, 1.8)

        def update(self):
            if not self.active:
                return
            self.y += self.vy
            self.vy += 0.6
            if self.y >= GROUND_Y - 10:
                self.explode()

        def explode(self):
            if self.exploded:
                return
            self.exploded = True
            self.active = False

        def draw(self, screen):
            if self.active:
                pygame.draw.circle(screen, (80, 80, 80), (int(self.x), int(self.y)), 12)
                pygame.draw.circle(screen, (180, 60, 60), (int(self.x), int(self.y)), 6)


    class Firework:
        """花火: 打ち上げてから炸裂する簡易花火エフェクト"""

        def __init__(self, x, base_y):
            self.x = x
            self.y = base_y
            self.vy = random.uniform(-12.0, -8.0)
            self.active = True
            self.phase = "ascend"
            self.particles = []
            self.created = time.time()

        def update(self):
            if self.phase == "ascend":
                self.y += self.vy
                self.vy += 0.5
                if self.vy > -2.5:
                    self.phase = "burst"
                    count = random.randint(20, 40)
                    for _ in range(count):
                        angle = random.uniform(0, math.pi * 2)
                        speed = random.uniform(2.5, 7.0)
                        pv = {
                            "x": self.x,
                            "y": self.y,
                            "vx": math.cos(angle) * speed,
                            "vy": math.sin(angle) * speed,
                            "life": random.uniform(0.9, 1.8),
                            "created": time.time(),
                            "color": (random.randint(200, 255), random.randint(100, 255), random.randint(50, 255))
                        }
                        self.particles.append(pv)
            elif self.phase == "burst":
                alive = []
                for p in self.particles:
                    age = time.time() - p["created"]
                    if age < p["life"]:
                        p["vx"] *= 0.995
                        p["vy"] += 0.12
                        p["x"] += p["vx"]
                        p["y"] += p["vy"]
                        alive.append(p)
                self.particles = alive
                if not self.particles:
                    self.active = False

        def draw(self, surface):
            if self.phase == "ascend":
                pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), 3)
            else:
                for p in self.particles:
                    age = time.time() - p["created"]
                    alpha = max(0, 255 - int((age / p["life"]) * 255))
                    surf = pygame.Surface((6, 6), pygame.SRCALPHA)
                    surf.fill((*p["color"], alpha))
                    surface.blit(surf, (int(p["x"]), int(p["y"])))


    class MagicCircle:
        """簡易的な魔法陣エフェクト（回転するリング）"""

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.radius = 48
            self.angle = 0.0
            self.created = time.time()

        def update(self):
            self.angle += 0.08

        def draw(self, surface):
            r = int(self.radius + math.sin(time.time() - self.created) * 6)
            for i in range(4):
                a = self.angle + i * math.pi / 2
                ox = int(math.cos(a) * r)
                oy = int(math.sin(a) * r)
                pygame.draw.circle(surface, PURPLE, (int(self.x + ox), int(self.y + oy)), 6, 2)
            for i in range(6):
                a = self.angle + i * (math.pi * 2 / 6)
                sx = int(self.x + math.cos(a) * (r - 12))
                sy = int(self.y + math.sin(a) * (r - 12))
                ex = int(self.x + math.cos(a + 0.3) * (r - 4))
                ey = int(self.y + math.sin(a + 0.3) * (r - 4))
                pygame.draw.line(surface, WHITE, (sx, sy), (ex, ey), 2)


    class InputHandler:
        """Enterキーの入力判定ロジック（短押し/長押し/ダブルタップ）"""

        def __init__(self):
            self.key_down_time = 0
            self.key_up_time = 0
            self.is_pressing = False
            self.press_duration = 0
            self.last_tap_time = 0
            self.short_press_detected = False
            self.long_press_detected = False
            self.double_tap_detected = False
            self.is_holding = False

        def on_key_down(self):
            current_time = time.time()
            if not self.is_pressing:
                time_since_last_tap = current_time - self.key_up_time
                if time_since_last_tap < DOUBLE_TAP_THRESHOLD and self.key_up_time > 0:
                    self.double_tap_detected = True
                self.key_down_time = current_time
                self.is_pressing = True
                self.is_holding = False

        def on_key_up(self):
            current_time = time.time()
            if self.is_pressing:
                self.press_duration = current_time - self.key_down_time
                self.key_up_time = current_time
                self.is_pressing = False
                self.is_holding = False
                if self.press_duration < SHORT_PRESS_THRESHOLD:
                    self.short_press_detected = True
                elif self.press_duration > LONG_PRESS_THRESHOLD:
                    self.long_press_detected = True

        def update(self):
            if self.is_pressing:
                current_time = time.time()
                self.press_duration = current_time - self.key_down_time
                if self.press_duration > LONG_PRESS_THRESHOLD:
                    self.is_holding = True

        def consume_short_press(self):
            if self.short_press_detected:
                self.short_press_detected = False
                return True
            return False

        def consume_long_press(self):
            if self.long_press_detected:
                self.long_press_detected = False
                return True
            return False

        def consume_double_tap(self):
            if self.double_tap_detected:
                self.double_tap_detected = False
                return True
            return False

        def reset(self):
            self.short_press_detected = False
            self.long_press_detected = False
            self.double_tap_detected = False


    class Game:
        """メインゲームクラス"""
        def __init__(self):
            # ===== まず：AttributeError防止のため、属性を先に全部作る =====
            self.running = True

            self.score = 0
            self.last_score = 0
            self.state = TITLE_SCREEN

            self.player = None
            self.boss = None
            self.items = []
            self.lightnings = []
            self.fireballs = []
            self.player_projectiles = []
            self.particles = []
            self.burning_zones = []
            self.fireworks = []
            self.recent_strikes = []

            self.bombs = []
            self.last_bomb_time = time.time()

            self.screen_shake_timer = 0
            self.screen_shake_magnitude = 0

            self.selected_skill = None
            self.skill_armed = False
            self.skill_arm_time = 0.0
            self.magic_circle = None
            self.countdown_value = None
            self.countdown_start = 0

            self.input_handler = InputHandler()

            # 効果音属性（先に作る）
            self.enter_sound = None
            self.enter_channel = None
            self.boss_sfx = None
            self.boss_channel = None

            # ===== ここが「ボスが出ない」原因だった所：必ず初期化する =====
            self.timer = COLLECT_PHASE_TIME
            self.timer_start = time.time()
            self.last_lightning_time = time.time()

            self.skill_options = ["Mahou Kougeki", "Tama wo Tobasu", "Ikkiuchi"]
            self.skill_highlight_index = 0
            self.skill_highlight_timer = 0

            self.clear_start = 0
            self.clear_brightness = 0.0
            self.abyss_start = None

            # ===== pygame 初期化（画像ロードより先に必要）=====
            pygame.init()
            try:
                pygame.mixer.init()
                pygame.mixer.set_num_channels(32)
            except Exception:
                pass

            pygame.display.set_caption(GAME_TITLE)
            self.screen = create_display((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.clock = pygame.time.Clock()

            # ===== 画面を作った後に画像ロード（convert_alpha対策）=====
            self.image_loader = ImageLoader()
            self.image_loader.load_image("player", PLAYER_IMG_PATH, (PLAYER_SIZE, PLAYER_SIZE))
            self.image_loader.load_image("boss",   BOSS_IMG_PATH,   (140, 140))
            self.image_loader.load_image("item",   ITEM_IMG_PATH,   (60, 60))

            # ===== フォント =====
            self.font_large = pygame.font.Font(None, 72)
            self.font_medium = pygame.font.Font(None, 40)
            self.font_small = pygame.font.Font(None, 28)

            if JP_FONT_PATH and Path(JP_FONT_PATH).exists():
                self.font_jp = pygame.font.Font(str(JP_FONT_PATH), 28)
                self.font_jp_large = pygame.font.Font(str(JP_FONT_PATH), 44)
                self.font_title = pygame.font.Font(str(JP_FONT_PATH), 72)
            else:
                # フォントが無い場合のフォールバック（豆腐の可能性あり）
                self.font_jp = self.font_small
                self.font_jp_large = self.font_medium
                self.font_title = self.font_large

            # ===== BGM / 効果音 =====
            try:
                if pygame.mixer.get_init() is None:
                    try:
                        pygame.mixer.init()
                    except Exception:
                        pass

                if os.path.exists(BGM_PATH):
                    try:
                        pygame.mixer.music.load(BGM_PATH)
                        pygame.mixer.music.set_volume(0.6)
                        pygame.mixer.music.play(-1)
                    except Exception:
                        pass

                if os.path.exists(ENTER_SFX_PATH):
                    try:
                        self.enter_sound = pygame.mixer.Sound(ENTER_SFX_PATH)
                        try:
                            self.enter_channel = pygame.mixer.Channel(6)
                        except Exception:
                            self.enter_channel = None
                    except Exception:
                        self.enter_sound = None
                        self.enter_channel = None

                if os.path.exists(BOSS_SFX_PATH):
                    try:
                        self.boss_sfx = pygame.mixer.Sound(BOSS_SFX_PATH)
                        try:
                            self.boss_channel = pygame.mixer.Channel(7)
                        except Exception:
                            self.boss_channel = None
                    except Exception:
                        self.boss_sfx = None
                        self.boss_channel = None

            except Exception:
                self.enter_sound = None
                self.enter_channel = None
                self.boss_sfx = None
                self.boss_channel = None

        def _play_boss_attack_sfx(self):
            if not self.boss_sfx:
                return
            try:
                if self.boss_channel:
                    if self.boss_channel.get_busy():
                        self.boss_channel.stop()
                    self.boss_channel.play(self.boss_sfx)
                else:
                    self.boss_sfx.play()
            except Exception:
                pass

        def reset_game(self):
            self.player = Player(self.image_loader)
            self.boss = Boss(self.image_loader)
            self.items = []
            self.lightnings = []
            self.timer = COLLECT_PHASE_TIME
            self.timer_start = time.time()
            self.last_lightning_time = time.time()
            self.selected_skill = None
            self.magic_circle = None
            self.countdown_value = None
            self.fireballs = []
            self.player_projectiles = []
            self.particles = []

            self.burning_zones = []
            self.fireworks = []
            self.score = 0
            self.bombs = []
            self.last_bomb_time = time.time()
            self.abyss_start = None

            self.skill_armed = False
            self.skill_arm_time = 0.0

            self.screen_shake_timer = 0
            self.screen_shake_magnitude = 0

            attempts = 0
            placed = 0
            target_count = 18
            min_sep = 48
            xs = []
            while placed < target_count and attempts < 2000:
                attempts += 1
                x = random.randint(120, WINDOW_WIDTH - 120)
                ok = True
                for ox in xs:
                    if abs(ox - x) < min_sep:
                        ok = False
                        break
                if not ok:
                    continue
                y = random.randint(-600, -80)
                self.items.append(Item(x, y, self.image_loader))
                xs.append(x)
                placed += 1
        
        def go_to_title(self):
            # 入力の残りを完全に無効化
            self.input_handler.reset()
            self.input_handler.is_pressing = False

            # 演出・残留物を全消し
            self.screen_shake_timer = 0
            self.screen_shake_magnitude = 0
            self.clear_brightness = 0.0
            self.clear_start = 0

            self.fireworks = []
            self.particles = []
            self.burning_zones = []
            self.lightnings = []
            self.bombs = []
            self.fireballs = []
            self.player_projectiles = []
            self.recent_strikes = []

            # 状態関連の残りを消す
            for attr in ("clear_to_score_time", "over_to_score_time", "clear_anim_start", "clear_wait_start"):
                if hasattr(self, attr):
                    delattr(self, attr)

            self.abyss_start = None
            self.magic_circle = None
            self.selected_skill = None
            self.skill_armed = False

            # タイトルではゲームオブジェクトを持たない（残骸による誤判定防止）
            self.player = None
            self.boss = None
            self.items = []


            # タイトルへ
            self.state = TITLE_SCREEN


        def handle_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.input_handler.on_key_down()

                        # Enter効果音（必要なら）
                        if getattr(self, "enter_sound", None):
                            try:
                                if self.enter_channel:
                                    if self.enter_channel.get_busy():
                                        self.enter_channel.stop()
                                    self.enter_channel.play(self.enter_sound)
                                else:
                                    self.enter_sound.play()
                            except Exception:
                                pass

                    elif event.key == pygame.K_r:
                        if self.state == GAME_CLEAR:
                            self.go_to_title()
                        elif self.state in (GAME_OVER, SCORE_SCREEN):
                            # リトライ：即ゲームを作り直して回収パートへ
                            self.input_handler.reset()
                            self.input_handler.is_pressing = False
                            self.reset_game()
                            self.state = COLLECT_PHASE

                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        self.input_handler.on_key_up()





    #    def open_image_picker(self):
            """タイトル画面での長押しにより画像選択ダイアログを開く"""
    #        changed = False
    #        changed |= self.image_loader.set_image_from_dialog("player", (PLAYER_SIZE, PLAYER_SIZE))
    #        changed |= self.image_loader.set_image_from_dialog("boss", (140, 140))
    #        changed |= self.image_loader.set_image_from_dialog("item", (20, 20))
    #        if changed:
    #            print("選択した画像を読み込みました。")

        def spawn_basic_shot(self):
            """素早い通常射（弱めの弾）を生成"""
            if not self.player or not self.boss:
                return
            mp = MagicProjectile(
                self.player.x + PLAYER_SIZE / 2,
                self.player.y + PLAYER_SIZE / 2,
                self.boss.x + random.uniform(-10, 10),
                self.boss.y + random.uniform(-10, 10),
                speed=11,
                damage=getattr(self.player, "attack_power", 1),
                color=(160, 220, 255)
            )
            for _ in range(6):
                self.particles.append(Particle(mp.x + random.uniform(-6, 6), mp.y + random.uniform(-6, 6), (200, 230, 255), life=0.4))
            self.player_projectiles.append(mp)

        def process_lightnings(self):
            """Update all lightnings, create burning zones and strike effects on completion."""
            if not self.lightnings:
                return
            new_lightnings = []
            now = time.time()
            for lightning in self.lightnings:
                lightning.update()
                if not lightning.active:
                    strike_x, strike_y = lightning.strike_point
                    dur = max(6.0, 8.0 * lightning.intensity)
                    self.burning_zones.append(BurningZone(strike_x, strike_y, width=int(220 * lightning.intensity), duration=dur))
                    if self.player and not self.player.dead:
                        player_rect = self.player.get_rect()
                        zone_rect = pygame.Rect(strike_x - int(120 * lightning.intensity), strike_y - int(120 * lightning.intensity), int(240 * lightning.intensity), int(240 * lightning.intensity))
                        if player_rect.colliderect(zone_rect):
                            base = 1
                            dmg = max(1, int(round(base * lightning.damage_factor * (0.8 + lightning.intensity * 0.4))))
                            self.player.take_damage(dmg)
                    for _ in range(30 + int(30 * lightning.intensity)):
                        self.particles.append(Particle(strike_x + random.uniform(-80, 80), strike_y + random.uniform(-40, 40), ORANGE, life=random.uniform(0.8, 1.8)))
                    self.recent_strikes.append((now, lightning.intensity, strike_x, strike_y))
                else:
                    new_lightnings.append(lightning)
            self.lightnings = new_lightnings

        def process_bombs(self):
            now = time.time()
            if now - self.last_bomb_time > 8.0 + random.random() * 12.0:
                bx = random.randint(60, WINDOW_WIDTH - 60)
                self.bombs.append(Bomb(bx))
                self.last_bomb_time = now

            new_bombs = []
            for b in self.bombs:
                b.update()
                if b.exploded:
                    sx = int(b.x)
                    sy = GROUND_Y
                    dur = 5.0 * b.intensity
                    self.burning_zones.append(BurningZone(sx, sy, width=int(180 * b.intensity), duration=dur))
                    if self.player and not self.player.dead:
                        pr = self.player.get_rect()
                        zone_rect = pygame.Rect(sx - int(100 * b.intensity), sy - int(100 * b.intensity), int(200 * b.intensity), int(200 * b.intensity))
                        if pr.colliderect(zone_rect):
                            self.player.take_damage(int(1 + 3 * b.intensity))
                    for _ in range(20 + int(20 * b.intensity)):
                        self.particles.append(Particle(sx + random.uniform(-80, 80), sy + random.uniform(-20, 20), ORANGE, life=random.uniform(0.8, 1.6)))
                else:
                    new_bombs.append(b)
            self.bombs = new_bombs

        def update(self):
            self.input_handler.update()
            if self.state in (COLLECT_PHASE, BOSS_PHASE):
                self.process_lightnings()
                self.process_bombs()

            if self.player and self.player.hp <= 0 and self.state in (COLLECT_PHASE, BOSS_PHASE):
                self.last_score = self.score
                self.state = SCORE_SCREEN
                return

            if self.state == GAME_CLEAR_ANIM:
                try:
                    if hasattr(self, 'boss') and self.boss:
                        self.boss.y += self.boss_fall_vy
                        self.boss_fall_vy += 0.9
                        if random.random() < 0.25:
                            self.particles.append(Particle(self.boss.x + random.uniform(-30, 30), self.boss.y + random.uniform(-20, 20), (200, 160, 40), life=0.9))
                        if self.boss.y >= GROUND_Y - self.boss.radius:
                            if not getattr(self, 'clear_exploded', False):
                                sx = int(self.boss.x)
                                sy = int(GROUND_Y)
                                for _ in range(180):
                                    self.particles.append(Particle(sx + random.uniform(-180, 180), sy + random.uniform(-80, 80), random.choice([YELLOW, RED, ORANGE]), life=random.uniform(0.8, 2.0)))
                                for _ in range(12):
                                    fx = random.randint(200, WINDOW_WIDTH - 200)
                                    self.fireworks.append(Firework(fx, WINDOW_HEIGHT // 2))
                                self.clear_brightness = 1.0
                                self.clear_start = time.time()
                                self.screen_shake_timer = time.time()
                                self.screen_shake_magnitude = 36
                                self.clear_exploded = True
                                self.clear_to_score_time = time.time() + 2.0
                    else:
                        self.state = GAME_CLEAR
                except Exception:
                    traceback.print_exc()
                    self.state = GAME_CLEAR

            if self.state == GAME_CLEAR_ANIM and hasattr(self, 'clear_to_score_time') and time.time() > getattr(self, 'clear_to_score_time', 0):
                self.state = GAME_CLEAR
                self.clear_start = time.time()
                self.clear_brightness = 1.0

            if self.state == GAME_OVER and hasattr(self, 'over_to_score_time') and time.time() > getattr(self, 'over_to_score_time', 0):
                self.last_score = self.score
                self.state = SCORE_SCREEN

            #if self.state == SCORE_SCREEN:
                #if self.input_handler.consume_short_press():
                #    self.state = TITLE_SCREEN
                #    try:
                #        self.reset_game()
                #    except Exception:
                #        traceback.print_exc()
                # return

            if self.state == TITLE_SCREEN:
                self.update_title_screen()
            elif self.state == COLLECT_PHASE:
                self.update_collect_phase()
            elif self.state == BOSS_PHASE:
                self.update_boss_phase()
            elif self.state == GAME_CLEAR or self.state == GAME_OVER:
                self.update_end_state()

        def update_title_screen(self):
        # 長押しでの画像選択は一旦無効化
        # if self.input_handler.consume_long_press():
        #     self.open_image_picker()

            if self.input_handler.consume_short_press():
                self.reset_game()
                self.state = COLLECT_PHASE


        def update_collect_phase(self):
            elapsed = time.time() - self.timer_start
            self.timer = max(0, COLLECT_PHASE_TIME - int(elapsed))

            if self.timer <= 0:
                self.state = BOSS_PHASE
                self.skill_highlight_timer = time.time()
                return

            if self.input_handler.consume_double_tap():
                self.player.move_left()
            if self.input_handler.consume_short_press():
                self.player.move_right()
            if self.input_handler.consume_long_press() or self.input_handler.is_holding:
                self.player.jump()

            for item in self.items:
                item.update()

            self.player.update()
            if self.player.hp <= 0:
                self.last_score = self.score
                self.state = SCORE_SCREEN
                return

            player_rect = self.player.get_rect()
            for item in self.items:
                if not item.collected and player_rect.colliderect(item.get_rect()):
                    item.collected = True
                    self.player.collected_items += 1
                    if self.player:
                        self.player.recalc_stats()
                    self.score += 100
                    for _ in range(12):
                        self.particles.append(Particle(item.x, item.y, YELLOW, life=0.7))

            current_time = time.time()
            if current_time - self.last_lightning_time > LIGHTNING_INTERVAL:
                x = random.randint(50, WINDOW_WIDTH - 50)
                self.lightnings.append(Lightning(x))
                self.last_lightning_time = current_time

            for proj in self.player_projectiles:
                proj.update()
            self.player_projectiles = [p for p in self.player_projectiles if p.active]

            if self.input_handler.consume_double_tap():
                self.spawn_basic_shot()

            for p in self.particles:
                p.update()
            self.particles = [p for p in self.particles if not p.is_dead()]

            for zone in self.burning_zones:
                zone.update()
                if zone.active and self.player and not self.player.dead:
                    player_rect = self.player.get_rect()
                    zone_rect = pygame.Rect(zone.x, zone.y, zone.width, WINDOW_HEIGHT - zone.y)
                    if player_rect.colliderect(zone_rect):
                        self.player.take_damage(1 if random.random() < 0.02 else 0)
                        if self.player.hp <= 0:
                            self.trigger_game_over()
            self.burning_zones = [z for z in self.burning_zones if z.active]

        def update_boss_phase(self):
            current_time = time.time()

            if self.player and self.player.dead:
                pass

            self.boss.update()

            if current_time - self.boss.last_fire_time > self.boss.fire_interval:
                self.boss.last_fire_time = current_time
                self.boss.fire_interval = random.uniform(1.2, 3.0)
                self._play_boss_attack_sfx()
                choice = random.random()
                if choice < 0.5:
                    if self.player:
                        fb = Fireball(self.boss.x, self.boss.y, self.player.x + PLAYER_SIZE / 2, self.player.y + PLAYER_SIZE / 2, speed=random.uniform(4.5, 7.0))
                        self.fireballs.append(fb)
                elif choice < 0.85:
                    if self.player:
                        for i in range(5):
                            offset_x = (i - 2) * 40
                            tx = self.player.x + PLAYER_SIZE / 2 + offset_x + random.uniform(-20, 20)
                            ty = self.player.y + PLAYER_SIZE / 2 + random.uniform(-20, 20)
                            fb = Fireball(self.boss.x, self.boss.y, tx, ty, speed=random.uniform(5.0, 7.5))
                            self.fireballs.append(fb)
                else:
                    if self.player:
                        sx = int(self.player.x + PLAYER_SIZE / 2)
                        sy = GROUND_Y - random.randint(20, 60)
                        dur = random.uniform(4.0, 9.0)
                        self.burning_zones.append(BurningZone(sx, sy, width=random.randint(120, 260), duration=dur))
                        for _ in range(16):
                            self.particles.append(Particle(sx + random.uniform(-40, 40), sy + random.uniform(-20, 20), ORANGE, life=0.9))

            if self.selected_skill is None:
                if current_time - self.skill_highlight_timer > 0.5:
                    self.skill_highlight_index = (self.skill_highlight_index + 1) % len(self.skill_options)
                    self.skill_highlight_timer = current_time

                if self.input_handler.consume_short_press():
                    self.selected_skill = self.skill_options[self.skill_highlight_index]
                    self.skill_armed = True
                    self.skill_arm_time = current_time
                    if self.selected_skill == "Tama wo Tobasu":
                        self.countdown_value = 3
                        self.countdown_start = current_time
            else:
                if self.input_handler.consume_double_tap():
                    self.spawn_basic_shot()

                if self.skill_armed and self.input_handler.consume_short_press():
                    self.on_skill_selected()
                    self.skill_armed = False
                    self.selected_skill = None

                if self.selected_skill == "Mahou Kougeki" and self.magic_circle:
                    self.magic_circle.update()
                elif self.selected_skill == "Tama wo Tobasu" and self.countdown_value is not None:
                    elapsed = current_time - self.countdown_start
                    if elapsed < 1:
                        self.countdown_value = 3
                    elif elapsed < 2:
                        self.countdown_value = 2
                    elif elapsed < 3:
                        self.countdown_value = 1
                    elif elapsed < 4:
                        self.countdown_value = "GO!"
                    else:
                        if self.countdown_value is not None:
                            self.spawn_tama_orbs()
                        self.countdown_value = None
                        self.selected_skill = None
                        self.skill_armed = False

            for fb in self.fireballs:
                fb.update()
                if fb.active and self.player and fb.get_rect().colliderect(self.player.get_rect()):
                    fb.active = False
                    self.player.x = max(0, self.player.x - 120)
                    self.player.vel_x = -6
                    self.player.take_damage(1)
                    if self.player.hp <= 0:
                        self.trigger_game_over()
                    if self.player.collected_items > 0:
                        self.player.collected_items = max(0, self.player.collected_items - 1)
                    for _ in range(22):
                        self.particles.append(Particle(self.player.x + PLAYER_SIZE / 2, self.player.y + PLAYER_SIZE / 2, ORANGE, life=0.9))
                    self.screen_shake_timer = time.time()
                    self.screen_shake_magnitude = 10

            self.fireballs = [f for f in self.fireballs if f.active]

            for proj in self.player_projectiles:
                proj.update()
                if proj.active:
                    boss_rect = pygame.Rect(int(self.boss.x - self.boss.radius), int(self.boss.y - self.boss.radius), self.boss.radius * 2, self.boss.radius * 2)
                    if proj.get_rect().colliderect(boss_rect):
                        proj.active = False
                        damage = getattr(proj, "damage", 1)
                        self.boss.hp = max(0, self.boss.hp - damage)
                        self.score += 50 * int(damage)
                        for _ in range(18 + int(damage * 6)):
                            col = random.choice([YELLOW, ORANGE, RED])
                            self.particles.append(Particle(self.boss.x + random.uniform(-40, 40), self.boss.y + random.uniform(-40, 40), col, life=random.uniform(0.8, 1.6)))
                        ring = pygame.Surface((300, 300), pygame.SRCALPHA)
                        pygame.draw.circle(ring, (255, 200, 120, 40), (150, 150), 120)
                        self.screen.blit(ring, (int(self.boss.x - 150), int(self.boss.y - 150)), special_flags=pygame.BLEND_ADD)
                        self.screen_shake_timer = time.time()
                        self.screen_shake_magnitude = min(40, self.screen_shake_magnitude + 6)

            self.player_projectiles = [p for p in self.player_projectiles if p.active]

            for p in self.particles:
                p.update()
            self.particles = [p for p in self.particles if not p.is_dead()]

            for zone in self.burning_zones:
                zone.update()
                if zone.active and self.player and not self.player.dead:
                    player_rect = self.player.get_rect()
                    zone_rect = pygame.Rect(zone.x, zone.y, zone.width, WINDOW_HEIGHT - zone.y)
                    if player_rect.colliderect(zone_rect):
                        if random.random() < 0.04:
                            self.player.take_damage(1)
                        if self.player.hp <= 0:
                            self.trigger_game_over()
            self.burning_zones = [z for z in self.burning_zones if z.active]

            if time.time() - self.screen_shake_timer > 0.5:
                self.screen_shake_magnitude = max(0, self.screen_shake_magnitude - 0.5)

            if self.boss.hp <= 0:
                self.trigger_game_clear()

        def trigger_game_clear(self):
            if not hasattr(self, 'boss') or not self.boss:
                self.state = GAME_CLEAR_ANIM
                self.input_handler.reset()    # 追加：連打の残りを消す
                self.clear_brightness = 1.0
                self.clear_start = time.time()
                self.clear_wait_start = time.time()
                return
            self.clear_anim_start = time.time()
            self.clear_exploded = False
            self.boss_fall_vy = 2.0
            self.state = GAME_CLEAR_ANIM
            for _ in range(24):
                self.particles.append(Particle(self.boss.x + random.uniform(-40, 40), self.boss.y + random.uniform(-40, 40), YELLOW, life=random.uniform(0.6, 1.2)))

        def trigger_game_over(self):
            self.last_score = self.score
            self.abyss_start = time.time()
            for _ in range(8):
                x = random.randint(100, WINDOW_WIDTH - 200)
                y = GROUND_Y - random.randint(40, 10)
                dur = random.uniform(6.0, 12.0)
                self.burning_zones.append(BurningZone(x, y, width=random.randint(120, 320), duration=dur))
            for _ in range(80):
                self.particles.append(Particle(random.randint(50, WINDOW_WIDTH - 50), random.randint(50, GROUND_Y - 20), ORANGE, life=random.uniform(0.8, 1.8)))
            self.state = GAME_OVER
            self.over_to_score_time = time.time() + 3.5
            self.screen_shake_timer = time.time()
            self.screen_shake_magnitude = 22

        def on_skill_selected(self):
            if self.selected_skill == "Mahou Kougeki":
                self.magic_circle = MagicCircle(self.player.x + PLAYER_SIZE // 2, self.player.y + PLAYER_SIZE)
                mp = MagicProjectile(self.player.x + PLAYER_SIZE / 2, self.player.y + PLAYER_SIZE / 2, self.boss.x, self.boss.y, speed=10, damage=getattr(self.player, "attack_power", 1) + 1, color=(255, 220, 140))
                for _ in range(24):
                    self.particles.append(Particle(mp.x + random.uniform(-12, 12), mp.y + random.uniform(-12, 12), (255, 200, 120), life=0.9))
                self.player_projectiles.append(mp)
            elif self.selected_skill == "Tama wo Tobasu":
                pass
            elif self.selected_skill == "Ikkiuchi":
                self.boss.hp = max(0, self.boss.hp - 2)
                for _ in range(30):
                    self.particles.append(Particle(self.boss.x, self.boss.y, RED, life=1.0))
                self.screen_shake_timer = time.time()
                self.screen_shake_magnitude = 12

        def spawn_tama_orbs(self):
            """Tama wo Tobasu の発射処理（カウント終了後に複数弾をボスへ）"""
            for _ in range(8):
                orb = Orb(self.player.x + PLAYER_SIZE / 2, self.player.y + PLAYER_SIZE / 2, self.boss.x + random.uniform(-20, 20), self.boss.y + random.uniform(-20, 20), speed=random.uniform(5.5, 8.0), damage=getattr(self.player, "attack_power", 1))
                for _ in range(4):
                    self.particles.append(Particle(orb.x + random.uniform(-6, 6), orb.y + random.uniform(-6, 6), (220, 180, 255), life=0.5))
                self.player_projectiles.append(orb)

        def update_end_state(self):
            for fw in self.fireworks:
                fw.update()
            self.fireworks = [f for f in self.fireworks if f.active]

            for p in self.particles:
                p.update()
            self.particles = [p for p in self.particles if not p.is_dead()]

            for zone in self.burning_zones:
                zone.update()
            self.burning_zones = [z for z in self.burning_zones if z.active]

            if self.state == GAME_CLEAR:
                t = time.time() - self.clear_start
                self.clear_brightness = max(0.0, 1.0 - (t / 4.0))
                if random.random() < 0.02:
                    fx = random.randint(200, WINDOW_WIDTH - 200)
                    self.fireworks.append(Firework(fx, WINDOW_HEIGHT // 2))

        def draw(self):
            shake_x = shake_y = 0
            if self.screen_shake_magnitude > 0:
                shake_x = random.randint(-int(self.screen_shake_magnitude), int(self.screen_shake_magnitude))
                shake_y = random.randint(-int(self.screen_shake_magnitude), int(self.screen_shake_magnitude))

            self.screen.fill(DARK_GRAY)
            temp = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            temp.fill(DARK_GRAY)

            if self.state == TITLE_SCREEN:
                self.draw_title_screen(temp)
            elif self.state == COLLECT_PHASE:
                self.draw_collect_phase(temp)
            elif self.state == BOSS_PHASE or self.state == GAME_CLEAR_ANIM:
                if self.boss:
                    self.draw_boss_phase(temp)
                else:
                    self.draw_collect_phase(temp)
            elif self.state == GAME_CLEAR:
                if self.boss:
                    self.draw_boss_phase(temp)
                else:
                    self.draw_collect_phase(temp)
            elif self.state == GAME_OVER:
                if self.boss:
                    self.draw_boss_phase(temp)
                else:
                    self.draw_collect_phase(temp)

            for zone in self.burning_zones:
                zone.draw(temp)

            for proj in self.player_projectiles:
                proj.draw(temp)
            for b in self.bombs:
                b.draw(temp)
            for p in self.particles:
                p.draw(temp)
            for fb in self.fireballs:
                fb.draw(temp)
            for lightning in self.lightnings:
                lightning.draw(temp)

            for fw in self.fireworks:
                fw.draw(temp)

            if self.state == GAME_CLEAR and self.clear_brightness > 0:
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                alpha = int(180 * self.clear_brightness)
                overlay.fill((255, 255, 220, alpha))
                temp.blit(overlay, (0, 0))

            now = time.time()
            new_recent = []
            for (tstr, intensity, sx, sy) in getattr(self, 'recent_strikes', []):
                age = now - tstr
                if age < 0.45:
                    fade = 1.0 - (age / 0.45)
                    alpha = int(min(220, 220 * intensity * fade))
                    flash = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                    flash.fill((255, 255, 240, alpha))
                    temp.blit(flash, (0, 0))
                    rr = int(120 * intensity * (0.8 + 0.4 * fade))
                    glow = pygame.Surface((rr * 2, rr * 2), pygame.SRCALPHA)
                    pygame.draw.circle(glow, (255, 220, 140, int(alpha * 0.8)), (rr, rr), rr)
                    temp.blit(glow, (int(sx - rr), int(sy - rr)), special_flags=pygame.BLEND_ADD)
                    new_recent.append((tstr, intensity, sx, sy))
            self.recent_strikes = new_recent

            if self.state == GAME_OVER and self.abyss_start:
                t = now - self.abyss_start
                prog = min(1.0, t / 6.0)
                alpha = int(180 * prog)
                abyss = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                abyss.fill((8, 4, 20, alpha))
                rr = int(300 + prog * 800)
                glow = pygame.Surface((rr * 2, rr * 2), pygame.SRCALPHA)
                gcol = int(120 * (1.0 - prog))
                pygame.draw.circle(glow, (0, 0, 0, int(200 * prog)), (rr, rr), rr)
                abyss.blit(glow, (WINDOW_WIDTH // 2 - rr, WINDOW_HEIGHT // 2 - rr), special_flags=pygame.BLEND_RGBA_SUB)
                temp.blit(abyss, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                if random.random() < 0.08 + prog * 0.12:
                    px = random.randint(0, WINDOW_WIDTH)
                    py = random.randint(0, WINDOW_HEIGHT)
                    self.particles.append(Particle(px, py, (30, 0, 60), life=2.0))

            self.screen.blit(temp, (shake_x, shake_y))

            self.draw_overlay(self.screen)

            pygame.display.flip()

        def draw_overlay(self, surface):
            if self.state == COLLECT_PHASE:
                timer_text = self.font_large.render(f"Time: {self.timer}", True, WHITE)
                surface.blit(timer_text, (WINDOW_WIDTH // 2 - 140, 30))

            items_text = self.font_small.render(f"Items: {self.player.collected_items if self.player else 0}", True, WHITE)
            surface.blit(items_text, (30, 30))

            if self.player:
                bar_x = 30
                bar_y = 70
                bar_w = 260
                bar_h = 24
                pygame.draw.rect(surface, DARK_GRAY, (bar_x, bar_y, bar_w, bar_h))
                if self.player.max_hp > 0:
                    fill_w = int(bar_w * (self.player.hp / float(self.player.max_hp)))
                else:
                    fill_w = 0
                pygame.draw.rect(surface, GREEN, (bar_x, bar_y, fill_w, bar_h))
                pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_w, bar_h), 2)
                hp_text = self.font_small.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, WHITE)
                surface.blit(hp_text, (bar_x + 6, bar_y - 2))

            if self.state == COLLECT_PHASE:
                help_lines = [
                    "Enter 短押し: 前進",
                    "Enter 長押し: ジャンプ",
                    "Enter ダブルタップ: 左へ / 発射"
                ]
            elif self.state == BOSS_PHASE:
                if self.selected_skill is None:
                    help_lines = ["Enter 短押し: ワザを装填"]
                else:
                    help_lines = ["装填済み: Enter 短押しで発動"]
            elif self.state == TITLE_SCREEN:
                help_lines = ["[短押し Enter で開始]"]
            elif self.state == GAME_CLEAR:
                help_lines = ["GAME CLEAR!  R: タイトルへ / Esc: 終了"]
            elif self.state == GAME_OVER:
                help_lines = ["GAME OVER... R:リトライ / Esc:終了"]
            elif self.state == SCORE_SCREEN:
                help_lines = [f"Score: {getattr(self, 'last_score', self.score)}", "R:リトライ / Esc:終了"]
            else:
                help_lines = []

            x_right = WINDOW_WIDTH - 30
            y_top = 50
            for line in help_lines:
                text = self.font_jp.render(line, True, WHITE)
                surface.blit(text, (x_right - text.get_width(), y_top))
                y_top += 34

            if self.state == COLLECT_PHASE:
                legend_w = 520
                legend_h = 48
                lx = WINDOW_WIDTH // 2 - legend_w // 2
                ly = 110
                pygame.draw.rect(surface, (20, 20, 30), (lx - 8, ly - 8, legend_w + 16, legend_h + 16), border_radius=8)
                gap = legend_w // len(LIGHTNING_VARIANTS)
                for i, v in enumerate(LIGHTNING_VARIANTS):
                    cx = lx + i * gap + gap // 2
                    box_rect = pygame.Rect(cx - 28, ly, 56, 36)
                    pygame.draw.rect(surface, v["color"], box_rect, border_radius=6)
                    pygame.draw.rect(surface, WHITE, box_rect, 2, border_radius=6)
                    lab = f"x{v['factor']:.1f}"
                    t = self.font_small.render(lab, True, WHITE)
                    surface.blit(t, (cx - t.get_width() // 2, ly + 40 - 10))
                    tn = self.font_jp.render(v["name"], True, WHITE)
                    surface.blit(tn, (cx - tn.get_width() // 2, ly - 18))

            if self.state == GAME_CLEAR:
                text = self.font_large.render("GAME CLEAR", True, (255, 240, 200))
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 140))
                surface.blit(text, text_rect)

                sub = self.font_jp_large.render("世界はエンターキーの呪いから解放された", True, WHITE)
                sub_rect = sub.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
                surface.blit(sub, sub_rect)

                score_t = self.font_medium.render(f"Score: {self.score}", True, YELLOW)
                st_rect = score_t.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
                surface.blit(score_t, st_rect)

                hint1 = self.font_jp.render("R でタイトルに戻る", True, WHITE)
                hint2 = self.font_jp.render("Esc でゲーム一覧に戻る", True, WHITE)

                y = WINDOW_HEIGHT // 2 + 25
                surface.blit(hint1, (WINDOW_WIDTH // 2 - hint1.get_width() // 2, y))
                surface.blit(hint2, (WINDOW_WIDTH // 2 - hint2.get_width() // 2, y + 34))  
            
            elif self.state == GAME_OVER:
                text = self.font_large.render("世界は魔王に支配された...", True, (180, 30, 30))
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 120))
                surface.blit(text, text_rect)
                sub = self.font_jp_large.render("世界は消滅の淵にある", True, WHITE)
                sub_rect = sub.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
                surface.blit(sub, sub_rect)
                score_t = self.font_medium.render(f"Final Score: {self.score}", True, YELLOW)
                st_rect = score_t.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 10))
                surface.blit(score_t, st_rect)
                hint = self.font_jp.render("R:リトライ / Esc:終了", True, WHITE)
                surface.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT // 2 + 30))
            elif self.state == SCORE_SCREEN:
                title = self.font_large.render("SCORE", True, YELLOW)
                title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 120))
                surface.blit(title, title_rect)
                sc = getattr(self, 'last_score', self.score)
                score_t = self.font_jp_large.render(f"Final Score: {sc}", True, WHITE)
                st_rect = score_t.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
                surface.blit(score_t, st_rect)
                hint = self.font_jp.render("R:リトライ / Esc:終了", True, WHITE)
                surface.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT // 2 + 40))

        def draw_title_screen(self, surface):
            title_text = self.font_title.render(GAME_TITLE, True, WHITE)
            title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 140))
            surface.blit(title_text, title_rect)

            scenario_lines = [
                "So... you have awakened, Recorder.",
                "You were chosen to become the Administrator of the Eternal 30 Seconds.",
                "Now, fulfill your role and step forward.",
                "",
                "[Enter で開始]"
            ]

            y_offset = WINDOW_HEIGHT // 2 - 100
            for line in scenario_lines:
                text = self.font_jp.render(line, True, WHITE)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
                surface.blit(text, text_rect)
                y_offset += 48

        def draw_collect_phase(self, surface):
            pygame.draw.rect(surface, GRAY, (0, GROUND_Y, WINDOW_WIDTH, WINDOW_HEIGHT - GROUND_Y))

            for item in self.items:
                item.draw(surface)

            for lightning in self.lightnings:
                lightning.draw(surface)

            self.player.draw(surface)

        def draw_boss_phase(self, surface):
            pygame.draw.rect(surface, GRAY, (0, GROUND_Y, WINDOW_WIDTH, WINDOW_HEIGHT - GROUND_Y))

            self.boss.draw(surface)
            self.player.draw(surface)

            if self.magic_circle:
                self.magic_circle.draw(surface)

            self.draw_boss_hp(surface)

            if self.selected_skill is None:
                self.draw_skill_menu(surface)
            else:
                self.draw_skill_effect(surface)

        def draw_boss_hp(self, surface):
            bar_w = 420
            bar_h = 28
            bar_x = WINDOW_WIDTH - 40 - bar_w
            bar_y = 30
            pygame.draw.rect(surface, DARK_GRAY, (bar_x, bar_y, bar_w, bar_h))
            if self.boss.max_hp > 0:
                fill_w = int(bar_w * (self.boss.hp / float(self.boss.max_hp)))
            else:
                fill_w = 0
            pygame.draw.rect(surface, RED, (bar_x, bar_y, fill_w, bar_h))
            pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_w, bar_h), 3)
            t = self.font_small.render(f"BOSS: {self.boss.hp}/{self.boss.max_hp}", True, WHITE)
            surface.blit(t, (bar_x + 8, bar_y + (bar_h - t.get_height()) // 2))

        def draw_skill_menu(self, surface):
            menu_y = WINDOW_HEIGHT - 280

            for i, skill in enumerate(self.skill_options):
                if i == self.skill_highlight_index:
                    color = YELLOW
                    prefix = "> "
                else:
                    color = WHITE
                    prefix = "  "

                text = self.font_jp_large.render(f"{prefix}[ {skill} ]", True, color)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, menu_y + i * 72))
                surface.blit(text, text_rect)

        def draw_skill_effect(self, surface):
            if self.selected_skill == "Mahou Kougeki":
                text = self.font_jp_large.render("CHARGE chuu...", True, PURPLE)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 240))
                surface.blit(text, text_rect)

                gauge_width = 320
                gauge_height = 28
                gauge_x = WINDOW_WIDTH // 2 - gauge_width // 2
                gauge_y = WINDOW_HEIGHT - 200
                pygame.draw.rect(surface, GRAY, (gauge_x, gauge_y, gauge_width, gauge_height))
                fill_width = int(gauge_width * 0.6)
                pygame.draw.rect(surface, PURPLE, (gauge_x, gauge_y, fill_width, gauge_height))
                pygame.draw.rect(surface, WHITE, (gauge_x, gauge_y, gauge_width, gauge_height), 3)

            elif self.selected_skill == "Tama wo Tobasu" and self.countdown_value is not None:
                text = self.font_large.render(str(self.countdown_value), True, ORANGE)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                surface.blit(text, text_rect)

            elif self.selected_skill == "Ikkiuchi":
                text = self.font_jp_large.render("Ikkiuchi kaishi!", True, RED)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 240))
                surface.blit(text, text_rect)

        def run(self):
            while self.running:
                try:
                    self.handle_events()
                    self.update()
                    self.draw()
                    self.clock.tick(FPS)
                except Exception:
                    traceback.print_exc()

                    # ★二次エラー防止
                    self.last_score = getattr(self, "score", 0)
                    if not hasattr(self, "input_handler"):
                        self.input_handler = InputHandler()

                    self.go_to_title()


    if __name__ == "__main__":
        game = Game()
        game.run()














#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def 避けろ(high_score):
    #初期化
    pygame.init()
    pygame.mixer.init()
    if high_score is None:
        high_score = 0

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
    screen = create_display((W, H))# 指定したサイズのウィンドウを生成します
    screen.fill((240, 240, 240))


    # 使いたい変数や画像などをここで定義
    shougaibutu_img = pygame.image.load("作成されたゲーム/純真高等学校/避けろ！/asset/画像/24.png").convert_alpha() #透明化処理されている画像の部分が透明化になる
    shougaibutu_img=pygame.transform.scale(shougaibutu_img, (40, 160))
    coin_img=pygame.image.load("作成されたゲーム/純真高等学校/避けろ！/asset/画像/82.png").convert_alpha()
    coin_img=pygame.transform.scale(coin_img, (40, 40))
    character_fall_img=pygame.transform.scale(pygame.image.load("作成されたゲーム/純真高等学校/避けろ！/asset/画像/80.png"), (50, 50))
    character_rise_img=pygame.transform.scale(pygame.image.load("作成されたゲーム/純真高等学校/避けろ！/asset/画像/81.png"), (50, 50))
    scenery_img_1=pygame.image.load("作成されたゲーム/純真高等学校/避けろ！/asset/画像/12.png").convert_alpha()
    scenery_img_2=pygame.image.load("作成されたゲーム/純真高等学校/避けろ！/asset/画像/13.png").convert_alpha()
    scenery_img_3=pygame.image.load("作成されたゲーム/純真高等学校/避けろ！/asset/画像/14.png").convert_alpha()
    heart_img=pygame.image.load("作成されたゲーム/純真高等学校/避けろ！/asset/画像/136.png").convert_alpha()
    resistance_character_fall_img=pygame.transform.scale(pygame.image.load("作成されたゲーム/純真高等学校/避けろ！/asset/画像/80_white.png"), (50, 50))
    resistance_character_rise_img=pygame.transform.scale(pygame.image.load("作成されたゲーム/純真高等学校/避けろ！/asset/画像/81_white.png"), (50, 50))




    BGM_menu="作成されたゲーム/純真高等学校/避けろ！/asset/効果音・BGM/menu.mp3"
    BGM_rule="作成されたゲーム/純真高等学校/避けろ！/asset/効果音・BGM/rule.mp3"
    BGM_game="作成されたゲーム/純真高等学校/避けろ！/asset/効果音・BGM/game.mp3"
    choose_sound=pygame.mixer.Sound("作成されたゲーム/純真高等学校/避けろ！/asset/効果音・BGM/14.mp3")
    choose_sound.set_volume(0.3)
    decision_sound=pygame.mixer.Sound("作成されたゲーム/純真高等学校/避けろ！/asset/効果音・BGM/6.mp3")
    decision_sound.set_volume(0.3)
    start_sound=pygame.mixer.Sound("作成されたゲーム/純真高等学校/避けろ！/asset/効果音・BGM/13.mp3")
    start_sound.set_volume(0.3)
    accel_sound=pygame.mixer.Sound("作成されたゲーム/純真高等学校/避けろ！/asset/効果音・BGM/10.mp3")
    accel_sound.set_volume(0.3)
    damage_sound=pygame.mixer.Sound("作成されたゲーム/純真高等学校/避けろ！/asset/効果音・BGM/1.mp3")
    damage_sound.set_volume(0.3)
    get_coin_sound=pygame.mixer.Sound("作成されたゲーム/純真高等学校/避けろ！/asset/効果音・BGM/7.mp3")
    get_coin_sound.set_volume(0.3)
    get_heart_sound=pygame.mixer.Sound("作成されたゲーム/純真高等学校/避けろ！/asset/効果音・BGM/5.mp3")
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
                    return high_score
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
                            return high_score
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
                character_fall_img=pygame.transform.scale(pygame.image.load("作成されたゲーム/純真高等学校/避けろ！/asset/画像/80.png"), (50, 50))
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
    # while running が終わったら
    return high_score





    #次来た時にやること
    #回転する障害物をさっさと実装する
    #チュートリアルの時のポイントがメニューのポイント欄に表示させるバグが発生しています、要改善
    #上ができれば完成、BGMのほうから対応しな
    #タイトルや操作説明の所をさっさと作る





#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def OrderRecall():


    # --- ADD THIS: The name of your Japanese font file ---
    # Make sure this file is in the same folder as your script!
    JAPANESE_FONT = "NotoSansJP-Regular.ttf" # Or "NotoSansJP-Regular.ttf"

    def get_resource_path(filename):
        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, filename)

    pygame.init()

    # Screen settings
    WIDTH = 1920
    HEIGHT = 1080
    FPS = 60

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    BLUE = (100, 150, 255)

    # Game states
    STATE_MAIN_MENU = "menu"
    STATE_MEMORIZE = "memorize"
    STATE_FLIP_BACK = "flip_back"
    STATE_SHUFFLE = "shuffle"
    STATE_FLIP_FRONT = "flip_front"
    STATE_GUESS = "guess"
    STATE_RESULT = "result"
    STATE_COMPLETE = "complete"
    

    class Card:
        def __init__(self, x, y, image_name, card_id):
            self.x = x
            self.y = y
            self.target_x = x
            self.target_y = y
            self.card_id = card_id
            self.face_up = True
            self.selected = False
            
            scale_factor = min(WIDTH / 1920, HEIGHT / 1080)
            self.width = int(160 * scale_factor)
            self.height = int(160 * scale_factor)

            try:
                self.image = pygame.image.load(get_resource_path(image_name))
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            except Exception as e:
                print(f"Warning: Could not load {image_name}: {e}")
                self.image = pygame.Surface((self.width, self.height))
                self.image.fill((200, 200, 200))
                # Use the  font path here too for safety
                try:
                    font = pygame.font.Font(get_resource_path(JAPANESE_FONT), 36)
                except:
                    font = pygame.font.Font(None, 36)
                text = font.render(str(card_id + 1), True, BLACK)
                text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
                self.image.blit(text, text_rect)

        def draw(self, screen):
            if self.face_up:
                screen.blit(self.image, (int(self.x), int(self.y)))
                if self.selected:
                    pygame.draw.circle(screen, GREEN, 
                                    (int(self.x + self.width - 20), int(self.y + 20)), 15)
                    pygame.draw.circle(screen, WHITE, 
                                    (int(self.x + self.width - 20), int(self.y + 20)), 15, 3)
            else:
                pygame.draw.rect(screen, (50, 50, 150),
                            (int(self.x), int(self.y), self.width, self.height))
                pygame.draw.rect(screen, WHITE,
                            (int(self.x), int(self.y), self.width, self.height), 4)
        
        def move_towards_target(self, speed=8):
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.sqrt(dx**2 + dy**2)
            if dist > speed:
                self.x += (dx / dist) * speed
                self.y += (dy / dist) * speed
                return False
            else:
                self.x = self.target_x
                self.y = self.target_y
                return True

    class Game:
        def __init__(self):
            self.screen = create_display((WIDTH, HEIGHT))
            pygame.display.set_caption("オーダー・リコール (Order Recall)")
            self.clock = pygame.time.Clock()
            self.running = True

            try:
                self.background = pygame.image.load(get_resource_path("作成されたゲーム\九州情報大学\ORDER_RECALL\\background.png"))
                self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            except:
                self.background = pygame.Surface((WIDTH, HEIGHT))
                self.background.fill((30, 30, 60))

            # --- UPDATED: Load Japanese Font Files ---
            font_path = get_resource_path(JAPANESE_FONT)
            scale_factor = HEIGHT / 1080
            try:
                self.font_large = pygame.font.Font(font_path, int(96 * scale_factor))
                self.font_medium = pygame.font.Font(font_path, int(64 * scale_factor))
                self.font_small = pygame.font.Font(font_path, int(42 * scale_factor))
            except:
                print(f"ERROR: Could not find font file {JAPANESE_FONT}!")
                
            self.level = 1
            self.state = STATE_MAIN_MENU
            self.cards = []
            self.correct_order = []
            self.player_guesses = []
            self.cursor_index = 0
            self.cursor_speed = 2.0
            self.cursor_timer = 0
            self.cursor_order = []
            self.cursor_position = 0
            self.memorize_timer = 0
            self.memorize_duration = 6000  # Changed to 6 seconds
            self.flip_timer = 0
            self.flip_duration = 1000
            self.result_timer = 0
            self.result_duration = 2000  # Duration to show result before auto-continue
            self.shuffle_count = 0
            self.max_shuffles = 3
            self.complete_timer = 0
            self.complete_duration = 3000  # Duration to show completion before returning to menu

            self.level_images = {
                1: ["作成されたゲーム\九州情報大学\ORDER_RECALL\\1a.png", "作成されたゲーム\九州情報大学\ORDER_RECALL\\1b.png", "作成されたゲーム\九州情報大学\ORDER_RECALL\\1c.png", "作成されたゲーム\九州情報大学\ORDER_RECALL\\1d.png"],
                2: ["作成されたゲーム\九州情報大学\ORDER_RECALL\\2a.png", "作成されたゲーム\九州情報大学\ORDER_RECALL\\2b.png", "作成されたゲーム\九州情報大学\ORDER_RECALL\\2c.png", "作成されたゲーム\九州情報大学\ORDER_RECALL\\2d.png", "作成されたゲーム\九州情報大学\ORDER_RECALL\\2e.png"],
                3: ["作成されたゲーム\九州情報大学\ORDER_RECALL\\3a.png", "作成されたゲーム\九州情報大学\ORDER_RECALL\\3b.png", "作成されたゲーム\九州情報大学\ORDER_RECALL\\3c.png", "作成されたゲーム\九州情報大学\ORDER_RECALL\\3d.png", "作成されたゲーム\九州情報大学\ORDER_RECALL\\3e.png", "作成されたゲーム\九州情報大学\ORDER_RECALL\\3f.png"]
            }
            
            # Level-specific memorization text - UPDATED with "left to right"
            self.level_text = {
                1: "ドアの順番を左から右に覚えてください！",
                2: "車の順番を左から右に覚えてください！",
                3: "アヒルの順番を左から右に覚えてください！"
            }

        def setup_level(self):
            self.cards = []
            self.correct_order = []
            self.player_guesses = []
            self.cursor_index = 0
            self.cursor_timer = 0
            self.memorize_timer = 0
            self.shuffle_count = 0
            self.flip_timer = 0
            self.cursor_order = []
            self.cursor_position = 0
            images = self.level_images[self.level]
            if self.level == 1: self.cursor_speed = 2.0
            elif self.level == 2: self.cursor_speed = 1.8
            else: self.cursor_speed = 1.5
            scale_factor = min(WIDTH / 1920, HEIGHT / 1080)
            spacing = int(200 * scale_factor)
            total_width = len(images) * spacing - int(40 * scale_factor)
            start_x = (WIDTH - total_width) // 2
            y = HEIGHT // 2 - int(80 * scale_factor) + int(50 * scale_factor)
            
            # RANDOMIZE: Shuffle the images list to randomize initial placement
            randomized_images = images.copy()
            random.shuffle(randomized_images)
            
            for i, img in enumerate(randomized_images):
                card = Card(start_x + i * spacing, y, img, i)
                self.cards.append(card)
                self.correct_order.append(i)
            self.state = STATE_MEMORIZE

        def shuffle_cards(self):
            positions = [(card.x, card.y) for card in self.cards]
            random.shuffle(positions)
            for i, card in enumerate(self.cards):
                card.target_x, card.target_y = positions[i]

        def get_current_card_order(self):
            sorted_cards = sorted(enumerate(self.cards), key=lambda x: x[1].x)
            return [self.correct_order.index(card_id) + 1 for card_id, card in sorted_cards]

        def draw_cursor(self):
            if self.state == STATE_GUESS and len(self.player_guesses) < len(self.cards):
                card = self.cards[self.cursor_index]
                cursor_y = card.y - 50
                cursor_x = card.x + card.width // 2
                offset = math.sin(pygame.time.get_ticks() / 200) * 15
                pygame.draw.polygon(self.screen, YELLOW, [
                    (cursor_x, cursor_y + offset),
                    (cursor_x - 25, cursor_y - 30 + offset),
                    (cursor_x + 25, cursor_y - 30 + offset)
                ])
                progress = (self.cursor_timer % (self.cursor_speed * 1000)) / (self.cursor_speed * 1000)
                bar_width = card.width
                bar_height = 12
                bar_x = card.x
                bar_y = card.y + card.height + 15
                pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 3)
                pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, bar_width * progress, bar_height))

        def draw_ui(self):
            if self.state != STATE_MAIN_MENU:
                # Translated: Level
                level_text = self.font_medium.render(f"レベル: {self.level}/3", True, WHITE)
                self.screen.blit(level_text, (30, 30))
            
            if self.state == STATE_MEMORIZE:
                remaining = int((self.memorize_duration - self.memorize_timer) / 1000) + 1
                # Use level-specific text
                text = self.font_small.render(f"{self.level_text[self.level]} 残り {remaining} 秒", True, WHITE)
                self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200))
                
            elif self.state == STATE_GUESS:
                text = self.font_small.render(
                    f"タイミングよくスペースキーを押して選択！ ({len(self.player_guesses)}/{len(self.cards)})", 
                    True, WHITE)
                self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200))
                
                if len(self.player_guesses) > 0:
                    guess_text = "選択した順: "
                    for guess in self.player_guesses:
                        guess_text += f"{guess + 1} "
                    text = self.font_small.render(guess_text, True, YELLOW)
                    self.screen.blit(text, (30, HEIGHT - 70))

        def check_result(self):
            return self.player_guesses == self.correct_order

        def handle_input(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return high_score
                if event.type == pygame.KEYDOWN:
                    # Q key to quit game from anywhere
                    if event.key == pygame.K_q:
                        self.running = False
                    elif self.state == STATE_MAIN_MENU:
                        if event.key == pygame.K_SPACE:
                            self.setup_level()
                    elif event.key == pygame.K_ESCAPE:
                        self.level = 1
                        self.state = STATE_MAIN_MENU
                    elif event.key == pygame.K_SPACE:
                        if self.state == STATE_GUESS and len(self.player_guesses) < len(self.cards):
                            self.cards[self.cursor_index].selected = True
                            self.player_guesses.append(self.cursor_index)
                            if len(self.player_guesses) == len(self.cards):
                                self.state = STATE_RESULT
                                self.result_timer = pygame.time.get_ticks()
                        elif self.state == STATE_RESULT:
                            if self.check_result():
                                # Success - auto continue
                                if self.level < 3:
                                    self.level += 1
                                    self.setup_level()
                                else:
                                    self.state = STATE_COMPLETE
                                    self.complete_timer = pygame.time.get_ticks()
                            else:
                                # Failure - retry same level
                                self.setup_level()

        def update(self):
            dt = self.clock.get_time()
            if self.state == STATE_MEMORIZE:
                self.memorize_timer += dt
                if self.memorize_timer >= self.memorize_duration:
                    self.state = STATE_FLIP_BACK
                    self.flip_timer = 0
                    
            elif self.state == STATE_FLIP_BACK:
                self.flip_timer += dt
                if self.flip_timer >= self.flip_duration:
                    for card in self.cards: card.face_up = False
                    self.state = STATE_SHUFFLE
                    self.shuffle_cards()
                    
            elif self.state == STATE_SHUFFLE:
                all_reached = True
                for card in self.cards:
                    if not card.move_towards_target(8): all_reached = False
                if all_reached:
                    self.shuffle_count += 1
                    if self.shuffle_count < self.max_shuffles: 
                        self.shuffle_cards()
                    else:
                        self.state = STATE_FLIP_FRONT
                        self.flip_timer = 0
                        
            elif self.state == STATE_FLIP_FRONT:
                self.flip_timer += dt
                if self.flip_timer >= self.flip_duration:
                    for card in self.cards: card.face_up = True
                    self.state = STATE_GUESS
                    self.cursor_order = list(range(len(self.cards)))
                    random.shuffle(self.cursor_order)
                    self.cursor_index = self.cursor_order[0]
                    self.cursor_position = 0
                    
            elif self.state == STATE_GUESS:
                self.cursor_timer += dt
                if self.cursor_timer >= self.cursor_speed * 1000:
                    self.cursor_timer = 0
                    attempts = 0
                    while attempts < len(self.cards):
                        self.cursor_position = (self.cursor_position + 1) % len(self.cards)
                        self.cursor_index = self.cursor_order[self.cursor_position]
                        if self.cursor_index not in self.player_guesses: break
                        attempts += 1
                        
            elif self.state == STATE_RESULT:
                # Only auto-continue on success
                if self.check_result():
                    if pygame.time.get_ticks() - self.result_timer >= self.result_duration:
                        if self.level < 3:
                            self.level += 1
                            self.setup_level()
                        else:
                            self.state = STATE_COMPLETE
                            self.complete_timer = pygame.time.get_ticks()
                        
            elif self.state == STATE_COMPLETE:
                # Don't auto-return to menu - let player decide
                pass

        def draw(self):
            self.screen.blit(self.background, (0, 0))
            if self.state == STATE_MAIN_MENU:
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(180)
                overlay.fill(BLACK)
                self.screen.blit(overlay, (0, 0))
                
                title = self.font_large.render("オーダー・リコール", True, YELLOW)
                self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 250))
                
                pulse = abs(math.sin(pygame.time.get_ticks() / 400))
                alpha = int(155 + pulse * 100)
                play_text = self.font_medium.render("スペースキーで開始", True, GREEN)
                play_surface = pygame.Surface((play_text.get_width(), play_text.get_height()), pygame.SRCALPHA)
                play_surface.blit(play_text, (0, 0))
                play_surface.set_alpha(alpha)
                self.screen.blit(play_surface, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 - 100))
                
                restart_text = self.font_small.render("ESCキーでメニューに戻る (ゲーム中)", True, WHITE)
                self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - 20))
                
                quit_text = self.font_small.render("Qキーでゲーム終了", True, WHITE)
                self.screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 20))
                
                # UPDATED instructions with "left to right"
                instructions = [
                    "遊び方:",
                    "1. 絵の順番を左から右に覚える",
                    "2. シャッフルされるのを見る",
                    "3. カーソルが合った時に元の順番で選択する",
                    "4. 全3レベルをクリアして勝利！"
                ]
                y_offset = HEIGHT // 2 + 60
                for instruction in instructions:
                    text = self.font_small.render(instruction, True, WHITE)
                    self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
                    y_offset += 50
            else:
                for card in self.cards: card.draw(self.screen)
                self.draw_cursor()
                self.draw_ui()
                
                if self.state == STATE_RESULT:
                    overlay = pygame.Surface((WIDTH, HEIGHT))
                    overlay.set_alpha(200)
                    overlay.fill(BLACK)
                    self.screen.blit(overlay, (0, 0))
                    if self.check_result():
                        text = self.font_large.render("正解！", True, GREEN)
                        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 80))
                    else:
                        text = self.font_large.render("残念！", True, RED)
                        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 120))
                        # Show retry options for failure
                        retry_text = self.font_medium.render("スペースキーでリトライ", True, YELLOW)
                        menu_text = self.font_small.render("ESCキーでメニューに戻る", True, WHITE)
                        self.screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 20))
                        self.screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 90))
                        
                    correct_text = "正解の順番: " + " ".join(map(str, self.get_current_card_order()))
                    order_text = self.font_small.render(correct_text, True, YELLOW)
                    self.screen.blit(order_text, (WIDTH // 2 - order_text.get_width() // 2, HEIGHT // 2 + 160))
                
                elif self.state == STATE_COMPLETE:
                    overlay = pygame.Surface((WIDTH, HEIGHT))
                    overlay.set_alpha(220)
                    overlay.fill(BLACK)
                    self.screen.blit(overlay, (0, 0))
                    congrats = self.font_large.render("おめでとうございます！", True, GREEN)
                    msg1 = self.font_medium.render("全レベルをクリアしました！", True, YELLOW)
                    msg2 = self.font_medium.render("あなたは記憶力マスターです！", True, YELLOW)
                    menu_text = self.font_small.render("ESCキーでメニューに戻る", True, WHITE)
                    quit_text = self.font_small.render("Qキーでゲーム終了", True, WHITE)
                    self.screen.blit(congrats, (WIDTH // 2 - congrats.get_width() // 2, HEIGHT // 2 - 150))
                    self.screen.blit(msg1, (WIDTH // 2 - msg1.get_width() // 2, HEIGHT // 2 - 60))
                    self.screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2))
                    self.screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 80))
                    self.screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 130))
            pygame.display.flip()

        def run(self):
            while self.running:
                self.handle_input()
                self.update()
                self.draw()
                self.clock.tick(FPS)
            

    Game().run()
    return


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def Quick_Draw():
        # OS判定と適切な設定適用
    if sys.platform == "win32": # Windows 
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
        #DPIスケール無効化 
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform == "darwin": # macOS
        os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("linux"): # Linux 
        os.environ[ 
    'SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR'] = '0' 
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    elif sys.platform.startswith("freebsd") or sys.platform.startswith("openbsd") or sys.platform.startswith("netbsd"): # BSD系
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    
    elif sys.platform.startswith("sunos"): # Solaris 
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("haiku"): # Haiku OS 
        os.environ['SDL_VIDEO_WINDOW_POS'] = '50,50'
    elif sys.platform.startswith("android"): # Android 
        os.environ['SDL_VIDEO_CENTERED'] = '1' 
        os.environ['SDL_VIDEODRIVER'] = 'android' # Android専用設定
    elif sys.platform.startswith("emscripten"): #WebAssembly 
        print("Emscripten (WebAssembly) 環境:追加設定不要")
    elif sys.platform.startswith("cygwin") or sys.platform.startswith("msys"): # Cygwin / MSYS2 
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("riscos"): # RISC OS 
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("aix"): # IBM AIX 
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("vxworks"):
        # VxWorks
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("os2"): # 05/2 os.environ ['SDL_VIDEO_CENTERED'] = '1'
        pass
    elif sys.platform.startswith("amiga"):
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    # AmigaOS / Morphos
    else: # その他の未知のos
        print(f"警告: このOS ({sys.platform})は未検証です。動作しない可能性があります。")

    # 画面サイズ
    WIDTH , HEIGHT = 1920 , 1080

    #初期化
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load("作成されたゲーム/九州情報大学/Quick_Draw/asset/sounds/bgm.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)


    #ウィンドウ作成

    win = create_display((WIDTH, HEIGHT))
    pygame.display.set_caption("Quick Draw")
    clock = pygame.time.Clock()
    result_time = 0



    #日本語フォントの設定
    font_path = "NotoSansJP-Regular.ttf"
    font_size = 50
    try:
        font = pygame.font.Font(font_path, font_size)
    except Exception:
        font = pygame.font.SysFont(None, font_size)
    line_spacing = 20

    # フォントキャッシュ
    font_cache = {font_size: font}

    #音
    fire_se = pygame.mixer.Sound("作成されたゲーム/九州情報大学/Quick_Draw/asset/sounds/fire.mp3")
    shot_se = pygame.mixer.Sound("作成されたゲーム/九州情報大学/Quick_Draw/asset/sounds/shot.mp3")
    win_se  = pygame.mixer.Sound("作成されたゲーム/九州情報大学/Quick_Draw/asset/sounds/seikou.mp3")
    lose_se = pygame.mixer.Sound("作成されたゲーム/九州情報大学/Quick_Draw/asset/sounds/sippai.mp3")

    start_sound_played = False
    start_se = pygame.mixer.Sound("作成されたゲーム/九州情報大学/Quick_Draw/asset/sounds/start.mp3")

    #スタートボタンの設定
    try:
        start_btn_img = pygame.image.load("作成されたゲーム/九州情報大学/Quick_Draw/asset/image/start_btn.png").convert_alpha()
        start_btn_img = pygame.transform.scale(start_btn_img, (600, 300))
    except Exception:
        start_btn_img = pygame.Surface((600, 300))
        start_btn_img.fill((80, 80, 80))
    start_btn_rect = start_btn_img.get_rect(center=(WIDTH//2, HEIGHT//2 +100))
    # 画像サイズ取得
    width, height = start_btn_img.get_size()
    # スタートボタンテキスト表示
    start_text = font.render("START", True, (255, 255, 255), None)
    start_text_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
    win.blit(start_text, start_text_rect)

    # リスタートボタンテキスト表示
    restart_text = font.render("RESTART", True, (255, 255, 255), None)
    restart_text_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))

    #打撃ボタンの設定
    dageki_btn_img = None
    try:
        dageki_btn_img = pygame.image.load("作成されたゲーム/九州情報大学/Quick_Draw/asset/image/dageki_btn.png").convert_alpha()
        dageki_btn_img = pygame.transform.scale(dageki_btn_img, (500, 500))
    except Exception:
        dageki_btn_img = pygame.Surface((500, 500))
        dageki_btn_img.fill((120, 120, 120))
    dageki_btn_rect = dageki_btn_img.get_rect(center=(WIDTH//2, HEIGHT//2 +100))

    def load_background():
        background_path = "作成されたゲーム/九州情報大学/Quick_Draw/asset/image/cackgrond.png"
        if os.path.exists(background_path):
            try:
                img = pygame.image.load(background_path)
                img = img.convert()
                return pygame.transform.scale(img, (WIDTH, HEIGHT))
            except Exception as e:
                print(f"警告: 背景画像の読み込みに失敗しました: {background_path} -> {e}")
        s = pygame.Surface((WIDTH, HEIGHT))
        s.fill((30, 30, 30))
        return s

    bg_img = load_background()


    # 色
    WHITE = (255, 255, 255) 
    RED = (255, 100, 100)
    GREEN = (100, 255, 100)
    BLACK = (0, 0, 0)

    # 状態
    state = "start"
    rounds = 0
    player_wins = 0
    enemy_wins = 0

    #タイミング設定
    fire_time = 0
    reaction_time = 0
    player_shot = False
    fire_sound_played = False

    def draw_text(text, color, y_offset=0, size=None):
        nonlocal font, font_path, font_size, font_cache
        if size is not None:
            temp_font = font_cache.get(size)
            if temp_font is None:
                try:
                    temp_font = pygame.font.Font(font_path, size)
                except Exception:
                    temp_font = pygame.font.SysFont(None, size)
                font_cache[size] = temp_font
        else:
            temp_font = font
        text_surface = temp_font.render(text, True, color)
        rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
        win.blit(text_surface, rect)

    def draw_rule():
        rule = [
            "<ルール説明>", 
            "startボタンでゲーム開始！",
            "「Fire！」が表示されたら打撃ボタンを押そう！",
            "フライングは負けになるよ！",
            "5本勝負！先に3勝した方が勝ち！",
            "Escキーでゲーム終了",
        ]
        for i , line in enumerate(rule):
            text_surface = font.render(line, True, BLACK)
            rect = text_surface.get_rect(center=(WIDTH//2, 50 + i * 50))
            win.blit(text_surface, rect)

    def reset_round():
        nonlocal state, fire_time, player_shot, fire_sound_played
        state = "wait"
        fire_time = time.perf_counter() + random.randint(2 , 5)
        player_shot = False
        fire_sound_played = False

    #メイン部分
    running = True
    while running:
        if 'bg_img' in locals() and bg_img is not None:
            win.blit(bg_img, (0, 0))
        else:
            win.fill(BLACK)
        now = time.perf_counter()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #ESCキーでゲーム終了
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            #判定
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "start" and start_btn_rect.collidepoint(event.pos):
                    player_wins = 0
                    enemy_wins = 0
                    if not start_sound_played:
                        start_se.play()
                        start_sound_played = True
                    start_sound_played = False
                    reset_round()
                elif state == "end" and start_btn_rect.collidepoint(event.pos):
                    state = "start"
                    if not start_sound_played:
                        start_se.play()
                        start_sound_played = True
                    start_sound_played = False
                elif state == "wait" and dageki_btn_rect.collidepoint(event.pos):
                    # フライング負け
                    player_shot = True
                    enemy_wins += 1
                    result_message = "Too Early!"
                    result_color = RED
                    result_time = time.perf_counter()
                    state = "result"
                    try:
                        lose_se.play()
                    except Exception:
                        pass
                elif state == "fire" and dageki_btn_rect.collidepoint(event.pos) and not player_shot:
                    # 正常の射撃判定
                    reaction_time = (time.perf_counter() - fire_time) * 1000
                    player_shot = True
                    try:
                        shot_se.play()
                    except Exception:
                        pass
                    if reaction_time < 450:
                        player_wins += 1
                        result_message = "You Win! %.2fms" % (reaction_time)
                        result_color = GREEN
                        try:
                            win_se.play()
                        except Exception:
                            pass
                    else:
                        enemy_wins += 1
                        result_message = "You Lose!"
                        result_color = RED
                        try:
                            lose_se.play()
                        except Exception:
                            pass
                    state = "result"
                    result_time = time.perf_counter()


        #画面出力
        if state == "start":
            draw_rule()
            win.blit(start_btn_img, start_btn_rect)


            win.blit(start_text, start_text_rect)
        elif state == "wait":
            draw_text("Ready...", BLACK , -220 , size=100)
            if now >= fire_time:
                state = "fire"
            win.blit(dageki_btn_img, dageki_btn_rect)
        elif state == "fire":
            draw_text("FIRE!", RED , -220 , size=100)
            if not fire_sound_played:
                try:
                    fire_se.play()
                except Exception:
                    pass
                fire_sound_played = True
            win.blit(dageki_btn_img, dageki_btn_rect)
        elif state == "result":
            if 'bg_img' in locals() and bg_img is not None:
                win.blit(bg_img, (0, 0))
            else:
                win.fill(BLACK)
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            win.blit(overlay, (0, 0))
            draw_text(result_message, result_color, y_offset=0, size=100)
            if time.perf_counter() - result_time > 2:
                if player_wins == 3:
                    state = "end"
                elif enemy_wins == 3:
                    state = "end"
                else:
                    reset_round()
        elif state == "end":

            draw_text("ゲーム終了", BLACK, y_offset=-290, size=100)
            if player_wins == 3:
                draw_text(f"君の勝ち! {player_wins} - {enemy_wins}", (0, 255, 150), y_offset=-200, size=100)
            else:
                draw_text(f"君の負け... {player_wins} - {enemy_wins}", (255, 0, 0), y_offset=-200, size=100)
            draw_text("リスタートボタンを押してください", BLACK, y_offset=-110, size=100)
            win.blit(start_btn_img, start_btn_rect)
            win.blit(restart_text, restart_text_rect)

        pygame.display.update()
        clock.tick(60)
  

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def shampoo():

    # OS判定と適切な設定適用
    if sys.platform == "win32": # Windows 
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
        #DPIスケール無効化 
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform == "darwin": # macOS
        os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("linux"): # Linux 
        os.environ[ 
    'SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR'] = '0' 
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    elif sys.platform.startswith("freebsd") or sys.platform.startswith("openbsd") or sys.platform.startswith("netbsd"): # BSD系
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    
    elif sys.platform.startswith("sunos"): # Solaris 
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("haiku"): # Haiku OS 
        os.environ['SDL_VIDEO_WINDOW_POS'] = '50,50'
    elif sys.platform.startswith("android"): # Android 
        os.environ['SDL_VIDEO_CENTERED'] = '1' 
        os.environ['SDL_VIDEODRIVER'] = 'android' # Android専用設定
    elif sys.platform.startswith("emscripten"): #WebAssembly 
        print("Emscripten (WebAssembly) 環境:追加設定不要")
    elif sys.platform.startswith("cygwin") or sys.platform.startswith("msys"): # Cygwin / MSYS2 
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("riscos"): # RISC OS 
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("aix"): # IBM AIX 
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("vxworks"):
        # VxWorks
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("os2"): # 05/2 os.environ ['SDL_VIDEO_CENTERED'] = '1'
        pass
    elif sys.platform.startswith("amiga"):
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    # AmigaOS / Morphos
    else: # その他の未知のos
        print(f"警告: このOS ({sys.platform})は未検証です。動作しない可能性があります。")

    #基本設定
    W, H = 1920, 1080
    font_path = "NotoSansJP-Regular.ttf"
    FONT_SIZE = 32
    STEM_LENGTH_FACTOR = 2.0
    #ゲーム進行設定
    # 問題数やボーナス条件などの定数
    QUESTION_LIMIT = 15        # 全問数
    BONUS_THRESHOLD = 10       # 正解数がこれ以上でボーナス
    BONUS_TIME_SEC = 5         # ボーナスタイム秒数
    BONUS_POINTS_PER_PRESS = 20  # ボーナスタイム中の1回あたりの加点

    pygame.init()
    screen = create_display((W, H))
    pygame.display.set_caption("shampoo!")
    clock = pygame.time.Clock()

    #フォント設定
    def make_font(size):
        try:
            if font_path and os.path.isfile(font_path):
                return pygame.font.Font(font_path, size)
        except Exception:
            pass

        candidates = [
            "Meiryo",
            "Yu Gothic",
            "MS Gothic",
            "MS PGothic",
            "Noto Sans CJK JP",
            "TakaoPGothic",
            "TakaoGothic",
        ]
        for name in candidates:
            try:
                f = pygame.font.SysFont(name, size)
                if f:
                    return f
            except Exception:
                continue

        return pygame.font.SysFont(None, size)

    font = make_font(FONT_SIZE)
    font_small = make_font(24)
    font_large = make_font(48)

    def scale_image_keep_aspect(image, max_w, max_h):
        try:
            w, h = image.get_size()
            if w == 0 or h == 0:
                return image
            ratio = min(max_w / w, max_h / h)
            new_w = max(1, int(w * ratio))
            new_h = max(1, int(h * ratio))
            try:
                return pygame.transform.smoothscale(image, (new_w, new_h))
            except Exception:
                return pygame.transform.scale(image, (new_w, new_h))
        except Exception:
            return image

    #背景画像読み込み
    try:
        BACKGROUND_PATH = "作成されたゲーム/九州情報大学/shampoo/asset/images/background.png"
        if os.path.isfile(BACKGROUND_PATH):
            _bg = pygame.image.load(BACKGROUND_PATH).convert()
            BACKGROUND_IMAGE = pygame.transform.scale(_bg, (W, H))
        else:
            BACKGROUND_IMAGE = None
    except Exception:
        BACKGROUND_IMAGE = None




    def make_vector_button_surface(w, h, pressed=False, stem_length_factor=1.0):
        surf = pygame.Surface((w, h), pygame.SRCALPHA)

        # カラー設定
        bottle_color = (180, 220, 250)
        cap_color = (160, 200, 240)
        pump_color = (200, 230, 255)
        stem_color = (255, 255, 255)
        border_color = (100, 100, 100)

        # ボトル本体
        bottle_w = int(w * 0.4)
        bottle_h = int(h * 0.6)
        bottle_x = (w - bottle_w) // 2
        bottle_y = int(h * 0.35)
        br = int(min(w, h) * 0.2)
        pygame.draw.rect(surf, bottle_color, (bottle_x, bottle_y, bottle_w, bottle_h), border_radius=br)
        pygame.draw.rect(surf, border_color, (bottle_x, bottle_y, bottle_w, bottle_h), 2, border_radius=br)

        # キャップ
        cap_w = int(bottle_w * 0.5)
        cap_h = int(h * 0.05)
        cap_x = (w - cap_w) // 2
        cap_y = bottle_y - cap_h + 4
        pygame.draw.rect(surf, cap_color, (cap_x, cap_y, cap_w, cap_h), border_radius=cap_h // 2)
        pygame.draw.rect(surf, border_color, (cap_x, cap_y, cap_w, cap_h), 2, border_radius=cap_h // 2)

        # ポンプヘッド
        head_w = int(w * 0.15)
        head_h = int(h * 0.06)
        head_x = (w - head_w) // 2
        head_y = cap_y - head_h - 2
        if pressed:
            head_y += 4
        pygame.draw.rect(surf, pump_color, (head_x, head_y, head_w, head_h), border_radius=head_h // 2)
        pygame.draw.rect(surf, border_color, (head_x, head_y, head_w, head_h), 2, border_radius=head_h // 2)

        # ステム
        stem_w = max(2, int(w * 0.02))
        stem_h = max(2, int((cap_y - (head_y + head_h)) * stem_length_factor))
        stem_x = head_x + (head_w - stem_w) // 2
        stem_y = head_y + head_h
        pygame.draw.rect(surf, stem_color, (stem_x, stem_y, stem_w, stem_h))
        pygame.draw.rect(surf, border_color, (stem_x, stem_y, stem_w, stem_h), 1)

        # ノズル
        nozzle_w = int(head_w * 0.4)
        nozzle_h = int(h * 0.03)
        nozzle_x = head_x - nozzle_w + 4
        nozzle_y = head_y + head_h // 2 - nozzle_h // 2
        pygame.draw.rect(surf, pump_color, (nozzle_x, nozzle_y, nozzle_w, nozzle_h), border_radius=nozzle_h // 2)
        pygame.draw.rect(surf, border_color, (nozzle_x, nozzle_y, nozzle_w, nozzle_h), 2, border_radius=nozzle_h // 2)

        # 押下時
        if pressed:
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 30))
            surf.blit(overlay, (0, int(h * 0.02)))

        return surf


    #髪の画像ファイル（同じ画像を大きさを変えて使い分ける）
    HAIR_IMAGE_FILES = [
        "作成されたゲーム/九州情報大学/shampoo/asset/images/ahiru.png",
        "作成されたゲーム/九州情報大学/shampoo/asset/images/hane.png",
        "作成されたゲーム/九州情報大学/shampoo/asset/images/pikopiko.png",
        "作成されたゲーム/九州情報大学/shampoo/asset/images/toge.png",
        "作成されたゲーム/九州情報大学/shampoo/asset/images/girl.png",
    ]

    #表示倍率
    HAIR_IMAGE_MULTIPLIERS = [1.0, 2.0, 2.25, 1.25, 1.5]

    #髪のパターンデータ
    # (髪の長さスコア, サイズ, 推奨シャンプータイプレベル, image_index_in_IMAGE_PATHS, (min_presses, max_presses))
    HAIR_LENGTHS = [
        (5,  "1.0倍",  0, 2, (0, 1)),  #ほとんど不要
        (30, "1.5倍",  1, 1, (3, 5)),  #中くらい
        (35, "2.0倍",  1, 4, (2, 4)),  #中程度
        (40, "2.5倍",  2, 3, (4, 6)),  #やや多め
        (45, "3.0倍",  2, 0, (6, 8)),  #多め
    ]

    # メニュー画面
    def show_menu():
        if BACKGROUND_IMAGE:
            screen.blit(BACKGROUND_IMAGE, (0, 0))
        else:
            screen.fill((230, 240, 250))

        try:
            title_font = pygame.font.Font(font_path, 72)
        except Exception:
            title_font = pygame.font.SysFont(None, 72)
        title = title_font.render("shampoo!", True, (10, 10, 40))
        screen.blit(title, ((W - title.get_width()) // 2, H // 4))

        try:
            guide_font = pygame.font.Font(font_path, 28)
        except Exception:
            guide_font = pygame.font.SysFont(None, 28)
        guide_lines = [
            "Enterキーでゲーム開始",
            "ESCキーで終了します",
            "スペースで連打してシャンプーの量を調整！",
            "制限時間内に適切な回数を押して正解を目指そう！",
            "何度もプレイして適切なシャンプーの量を覚えよう！",
            f"全{QUESTION_LIMIT}問中{BONUS_THRESHOLD}問以上正解でボーナスタイム突入！",
            f"ボーナスタイム中は連打で{BONUS_POINTS_PER_PRESS}点ずつ加点！",
            "ハイスコアを目指して頑張ろう！",

        ]
        for i, line in enumerate(guide_lines):
            guide_text = guide_font.render(line, True, (40, 40, 40))
            screen.blit(guide_text, ((W - guide_text.get_width()) // 2, H // 2 + i * 40))

        pygame.display.flip()


    def show_countdown(seconds=3):
        for sec in range(seconds, 0, -1):
            start = pygame.time.get_ticks()
            screen.fill((20, 20, 40))
            try:
                title_font = pygame.font.Font(font_path, 72)
            except Exception:
                title_font = pygame.font.SysFont(None, 72)
            title = title_font.render("shampoo!", True, (255, 255, 255))
            screen.blit(title, ((W - title.get_width()) // 2, H // 4))

            num_text = font_large.render(str(sec), True, (255, 200, 50))
            screen.blit(num_text, ((W - num_text.get_width()) // 2, (H - num_text.get_height()) // 2))

            pygame.display.flip()

            # 1秒間イベント処理・待機
            while pygame.time.get_ticks() - start < 1000:
                for ev in pygame.event.get():
                    if ev.type == QUIT:
                        break
                    elif ev.type == KEYDOWN:
                        if ev.key == K_ESCAPE:
                            running = False


    # 本編
    def run_game():
        # スコア管理
        score = 0
        combo = 0
        max_combo = 0
        question_count = 0
        correct_count = 0
        game_running = True
        current_customer = None
        result_message = ""
        result_time = 0

        # 最終画面
        final_pending = False
        final_saved = False
        
        # ボタン押下管理
        button_press_count = 0  # 現在のボタン押下数
        button_press_feedback_time = 0 
        # ボーナスモード管理
        bonus_mode = False
        bonus_frames_remaining = 0
        bonus_press_count = 0
        bonus_score = 0
        # 次のあひるを保留
        next_customer_pending = False
        
        # あひるを生成
        def get_new_customer():
            # pick a pattern that now includes press range and image index
            hair_length, hair_name, required_shampoo, image_index, press_range = random.choice(HAIR_LENGTHS)
            customer_image = None
            image_path = None
            display_w = 200
            display_h = 300
            try:
                # image_index は HAIR_LENGTHS の4番目の要素として定義
                hair_image_index = image_index
                # 優先: 画像ごとの固定倍率があれば使用（indexに対応）
                try:
                    if 0 <= hair_image_index < len(HAIR_IMAGE_MULTIPLIERS):
                        multiplier = float(HAIR_IMAGE_MULTIPLIERS[hair_image_index])
                except Exception:
                    multiplier = None

                if 0 <= hair_image_index < len(HAIR_IMAGE_FILES):
                    candidate = HAIR_IMAGE_FILES[hair_image_index]
                    if candidate and os.path.isfile(candidate):
                        image_path = candidate
                        # 候補ファイルから倍率を決定できる場合は使う
                        if multiplier is None and candidate in HAIR_IMAGE_FILES:
                            try:
                                idx = HAIR_IMAGE_FILES.index(candidate)
                                if 0 <= idx < len(HAIR_IMAGE_MULTIPLIERS):
                                    multiplier = float(HAIR_IMAGE_MULTIPLIERS[idx])
                            except Exception:
                                pass
                        # 
                        if multiplier is None:
                            try:
                                if isinstance(hair_name, str) and hair_name.endswith("倍"):
                                    multiplier = float(hair_name.replace("倍", "").strip())
                                else:
                                    multiplier = max(0.1, float(hair_length) / 40.0)
                            except Exception:
                                multiplier = 1.0
                        display_w = max(1, int(200 * multiplier))
                        display_h = max(1, int(300 * multiplier))
                        customer_image = pygame.image.load(image_path).convert_alpha()
                        customer_image = scale_image_keep_aspect(customer_image, display_w, display_h)
                # fallback: pick any available HAIR_IMAGE_FILES image
                if customer_image is None:
                    fallback_path = None
                    if 0 <= image_index < len(HAIR_IMAGE_FILES) and os.path.isfile(HAIR_IMAGE_FILES[image_index]):
                        fallback_path = HAIR_IMAGE_FILES[image_index]
                    else:
                        for p in HAIR_IMAGE_FILES:
                            if p and os.path.isfile(p):
                                fallback_path = p
                                break
                    if fallback_path:
                        image_path = fallback_path
                        # fallback のファイルに対応する固定倍率を使えるなら使う
                        try:
                            idx = HAIR_IMAGE_FILES.index(fallback_path)
                            if 0 <= idx < len(HAIR_IMAGE_MULTIPLIERS):
                                multiplier = float(HAIR_IMAGE_MULTIPLIERS[idx])
                        except Exception:
                            pass
                        # まだ未決定なら HAIR_LENGTHS の名前や長さから推測
                        if multiplier is None:
                            try:
                                if isinstance(hair_name, str) and hair_name.endswith("倍"):
                                    multiplier = float(hair_name.replace("倍", "").strip())
                                else:
                                    multiplier = max(0.1, float(hair_length) / 40.0)
                            except Exception:
                                multiplier = 1.0
                        display_w = max(1, int(200 * multiplier))
                        display_h = max(1, int(300 * multiplier))
                        customer_image = pygame.image.load(image_path).convert_alpha()
                        customer_image = scale_image_keep_aspect(customer_image, display_w, display_h)
            except Exception:
                customer_image = None

                customer_image = None

            return {
                "hair_length": hair_length,
                "hair_name": hair_name,
                "required_shampoo": required_shampoo,
                "image_index": image_index,
                "image_path": image_path,
                "image": customer_image,
                "press_range": press_range,
                "display_size": (display_w, display_h),
                "display_multiplier": multiplier,
                "display_time": 0,
                # 制限時間: 5秒 -> 300フレーム
                "time_limit_frames": 300
            }
        
        current_customer = get_new_customer()

        # BGM と効果音の読み込み（存在するファイルを優先して使用）
        duck_sound = None
        correct_sound = None
        bonus_start_sound = None
        game_end_sound = None
        incorrect_sound = None

        try:
            bg_path = "作成されたゲーム/九州情報大学/shampoo/asset/sounds/backmusic.mp3"
            if not os.path.isfile(bg_path):
                bg_path = "作成されたゲーム/九州情報大学/shampoo/asset/sounds/5.mp3"
            if os.path.isfile(bg_path):
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(bg_path)
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.5)
        except Exception:
            pass

        # 効果音
        try:
            p = "作成されたゲーム/九州情報大学/shampoo/asset/sounds/6.mp3"  # 正解時
            if os.path.isfile(p):
                correct_sound = pygame.mixer.Sound(p)
        except Exception:
            correct_sound = None

        try:
            p = "作成されたゲーム/九州情報大学/shampoo/asset/sounds/7.mp3"  # ボーナスタイム開始時
            if os.path.isfile(p):
                bonus_start_sound = pygame.mixer.Sound(p)
        except Exception:
            bonus_start_sound = None

        try:
            p = "作成されたゲーム/九州情報大学/shampoo/asset/sounds/9.mp3"  # ボーナスタイム中の連打
            if os.path.isfile(p):
                bonus_press_sound = pygame.mixer.Sound(p)
        except Exception:
            bonus_press_sound = None

        try:
            p = "作成されたゲーム/九州情報大学/shampoo/asset/sounds/13.mp3"  # ゲーム終了時
            if os.path.isfile(p):
                game_end_sound = pygame.mixer.Sound(p)
        except Exception:
            game_end_sound = None

        try:
            p = "作成されたゲーム/九州情報大学/shampoo/asset/sounds/5.mp3"  # あひる表示時
            if os.path.isfile(p):
                duck_sound = pygame.mixer.Sound(p)
        except Exception:
            duck_sound = None
        # あひる出現時の効果音を再生
        try:
            if current_customer and duck_sound:
                duck_sound.play()
        except Exception:
            pass

        # ゲームループ
        while game_running:
            clock.tick(60)
            if current_customer:
                current_customer["display_time"] += 1
            
            if button_press_feedback_time > 0:
                button_press_feedback_time -= 1

            #制限時間で判定（5秒=300フレーム想定）
            if current_customer and current_customer.get("display_time", 0) >= current_customer.get("time_limit_frames", 300):
                question_count += 1
                min_presses, max_presses = current_customer.get("press_range", (0, 0))

                if min_presses <= button_press_count <= max_presses:
                    result_message = f"正解！{button_press_count}回"
                    correct_count += 1
                    combo += 1
                    max_combo = max(max_combo, combo)
                    score += 100 + (combo * 10)
                    if correct_sound:
                        correct_sound.play()
                else:
                    result_message = f"不正解 必要:{min_presses}-{max_presses}回 選択:{button_press_count}回"
                    combo = 0
                    if incorrect_sound:
                        incorrect_sound.play()

                #後処理（正解/不正解に関わらず）
                result_time = 90
                button_press_count = 0

                #次のあひる保留
                next_customer_pending = True

                #問題数が上限に達したらボーナス判定または終了処理
                if question_count >= QUESTION_LIMIT:
                    if correct_count >= BONUS_THRESHOLD:
                        bonus_mode = True
                        bonus_frames_remaining = BONUS_TIME_SEC * 60
                        bonus_press_count = 0
                        bonus_score = 0
                        result_message = "ボーナスタイム！連打でボーナスを稼ごう！"
                        result_time = 90
                        # 次のあひるは表示しない
                        current_customer = None
                        try:
                            if bonus_start_sound:
                                bonus_start_sound.play()
                        except Exception:
                            pass
                    else:
                        # ボーナスに届かない場合はゲーム終了
                        result_message = f"終了: {correct_count}/{QUESTION_LIMIT} 正解"
                        result_time = 180
                        current_customer = None
                        final_pending = True
                        try:
                            if game_end_sound:
                                game_end_sound.play()
                        except Exception:
                            pass
                else:
                    current_customer = None
            
            #最終画面用のリトライボタン
            retry_rect = pygame.Rect((W - 300) // 2, H // 2 + 40, 300, 80)

            #イベント処理
            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
                elif event.type == KEYDOWN:

                    if final_pending and result_time <= 0:
                        if event.key == K_ESCAPE:
                            return False
                        if event.key == K_r:
                            score = 0
                            combo = 0
                            max_combo = 0
                            question_count = 0
                            correct_count = 0
                            result_message = ""
                            result_time = 0
                            button_press_count = 0
                            button_press_feedback_time = 0
                            bonus_mode = False
                            bonus_frames_remaining = 0
                            bonus_press_count = 0
                            bonus_score = 0
                            current_customer = get_new_customer()
                            try:
                                if duck_sound:
                                    duck_sound.play()
                            except Exception:
                                pass
                            final_pending = False
                            final_saved = False

                            show_countdown(3)
                        continue

                    if event.key == K_ESCAPE:
                        return False
                    #スペースキーでの処理
                    elif event.key == K_SPACE:
                        #判定結果表示中はボタンを無効化
                        if result_time > 0:
                            continue
                        #ボーナスモード中はボーナス用のカウント
                        if bonus_mode:
                            bonus_press_count += 1
                            button_press_feedback_time = 10
                            try:
                                if bonus_press_sound:
                                    bonus_press_sound.play()
                            except Exception:
                                pass
                        else:

                            button_press_count += 1
                            button_press_feedback_time = 10

                elif event.type == MOUSEBUTTONDOWN:

                    if final_pending and result_time <= 0:
                        if event.button == 1:
                            if retry_rect.collidepoint(event.pos):
                                score = 0
                                combo = 0
                                max_combo = 0
                                question_count = 0
                                correct_count = 0
                                result_message = ""
                                result_time = 0
                                button_press_count = 0
                                button_press_feedback_time = 0
                                bonus_mode = False
                                bonus_frames_remaining = 0
                                bonus_press_count = 0
                                bonus_score = 0
                                current_customer = get_new_customer()
                                try:
                                    if duck_sound:
                                        duck_sound.play()
                                except Exception:
                                    pass
                                final_pending = False
                                final_saved = False
                                show_countdown(3)
                                continue
            
            # 画面描画
            if BACKGROUND_IMAGE:
                screen.blit(BACKGROUND_IMAGE, (0, 0))
            else:
                screen.fill((240, 250, 255))
            
            #スコア表示
            score_text = font.render(f"スコア: {score}", True, (0, 0, 0))
            screen.blit(score_text, (20, 20))
            
            combo_text = font_small.render(f"コンボ: {combo}", True, (0, 100, 200))
            screen.blit(combo_text, (20, 70))
            
            count_text = font_small.render(f"問題: {question_count} 正解: {correct_count}", True, (0, 0, 0))
            screen.blit(count_text, (20, 110))

            question_text = font_small.render(f"残りの問題数: {15-question_count}", True, (0, 0, 0))
            screen.blit(question_text, (20, 150))
            
            # あひるを表示
            if current_customer and current_customer.get("image"):
                ds = current_customer.get("display_size", (300, 450))
                ahiru_img = scale_image_keep_aspect(current_customer["image"], ds[0], ds[1])
                screen.blit(ahiru_img, ((W - ahiru_img.get_width()) // 2, 100))

            #ボーナスモード画面描画
            if bonus_mode:
                #ボーナスタイムの残り時間と現在の連打数を表示
                remain_sec = bonus_frames_remaining // 60
                remain_text = font_large.render(f"BONUS TIME: {remain_sec}s", True, (255, 200, 50))
                screen.blit(remain_text, ((W - remain_text.get_width()) // 2, 80))

                bonus_count_text = font_large.render(str(bonus_press_count), True, (255, 50, 50))
                screen.blit(bonus_count_text, ((W - bonus_count_text.get_width()) // 2, 180))
            
            # プッシュボタンを表示
            button_x = W // 2 - 260
            button_y = H // 2 + 40
            button_width = 260*2
            button_height = 180*2

            feedback_offset = 0
            if button_press_feedback_time > 0:
                feedback_offset = int(10 * (1 - button_press_feedback_time / 10))

            # ベクター描画を使う（いつも使いたい場合は True にする）
            USE_VECTOR_BUTTON = True
            if locals().get("BUTTON_IMAGE") and not USE_VECTOR_BUTTON:
                img_to_use = locals().get("BUTTON_IMAGE")
                if button_press_feedback_time > 0 and locals().get("BUTTON_PRESSED_IMAGE"):
                    img_to_use = locals().get("BUTTON_PRESSED_IMAGE")
                img_draw = scale_image_keep_aspect(img_to_use, button_width, button_height)
                img_x = button_x + (button_width - img_draw.get_width()) // 2
                img_y = button_y + feedback_offset
                screen.blit(img_draw, (img_x, img_y))
                #ボタンテキスト（画像に無い場合にのみ描画）
                button_text = font_large.render("PUSH", True, (255, 255, 255))
                screen.blit(button_text, (button_x + button_width // 2 - button_text.get_width() // 2, img_y + (button_height - button_text.get_height()) // 2))
            else:
                # ベクターで生成したボタン画像を使う（キャッシュして毎フレーム再生成を避ける）
                try:
                    if "_vector_button_cache" not in locals():
                        _vector_button_cache = {}
                except Exception:
                    _vector_button_cache = {}

                key = (button_width, button_height, STEM_LENGTH_FACTOR)
                if key not in _vector_button_cache:
                    _vector_button_cache[key] = (
                        make_vector_button_surface(button_width, button_height, pressed=False, stem_length_factor=STEM_LENGTH_FACTOR),
                        make_vector_button_surface(button_width, button_height, pressed=True, stem_length_factor=STEM_LENGTH_FACTOR)
                    )
                vec_normal, vec_pressed = _vector_button_cache[key]
                img_draw = vec_pressed if button_press_feedback_time > 0 else vec_normal
                img_x = button_x + (button_width - img_draw.get_width()) // 2
                img_y = button_y + feedback_offset + (4 if button_press_feedback_time > 0 else 0)
                screen.blit(img_draw, (img_x, img_y))

            
            # 現在の押回数を表示
            display_press_count = bonus_press_count if bonus_mode else button_press_count
            press_count_text = font_large.render(str(display_press_count), True, (255, 0, 0))
            screen.blit(press_count_text, (button_x + button_width // 2 - press_count_text.get_width() // 2, button_y + 270))
            
            #結果メッセージ
            if result_time > 0:
                if "正解" in result_message:
                    result_color = (0, 200, 0)
                else:
                    result_color = (200, 0, 0)
                
                result_text = font.render(result_message, True, result_color)
                screen.blit(result_text, ((W - result_text.get_width()) // 2, H // 2 - 100))
                
                result_time -= 1

            if result_time <= 0 and next_customer_pending and (not final_pending) and (not bonus_mode):
                current_customer = get_new_customer()
                try:
                    if duck_sound:
                        duck_sound.play()
                except Exception:
                    pass
                next_customer_pending = False

            #最終画面表示判定
            if final_pending and result_time <= 0:
                #最終画面描画
                if BACKGROUND_IMAGE:
                    screen.blit(BACKGROUND_IMAGE, (0, 0))
                else:
                    screen.fill((230, 230, 240))
                final_title = font_large.render("ゲーム終了", True, (10, 10, 40))
                screen.blit(final_title, ((W - final_title.get_width()) // 2, 120))

                final_score_text = font.render(f"最終スコア: {score}", True, (0, 0, 0))
                screen.blit(final_score_text, ((W - final_score_text.get_width()) // 2, 220))

                #リトライボタン
                retry_rect = pygame.Rect((W - 300) // 2, H // 2 + 40, 300, 80)
                pygame.draw.rect(screen, (100, 200, 100), retry_rect)
                pygame.draw.rect(screen, (0, 120, 0), retry_rect, 4)
                retry_text = font_large.render("リトライ", True, (255, 255, 255))
                screen.blit(retry_text, (retry_rect.x + (retry_rect.width - retry_text.get_width()) // 2,
                                        retry_rect.y + (retry_rect.height - retry_text.get_height()) // 2))

                hint_text = font_small.render("Rキーでもリトライ | ESCでメニューへ", True, (80, 80, 80))
                screen.blit(hint_text, ((W - hint_text.get_width()) // 2, retry_rect.y + retry_rect.height + 20))

                pygame.display.flip()
                continue

            # ボーナスモードの更新
            if bonus_mode:
                if bonus_frames_remaining > 0:
                    bonus_frames_remaining -= 1
                else:
                    # ボーナスタイム終了→スコア加算して終了
                    bonus_score = bonus_press_count * BONUS_POINTS_PER_PRESS
                    score += bonus_score
                    result_message = f"ボーナス +{bonus_score}点！"
                    result_time = 180
                    bonus_mode = False
                    final_pending = True
                    try:
                        if game_end_sound:
                            game_end_sound.play()
                    except Exception:
                        pass
            
            # 操作説明
            if bonus_mode:
                help_line = "ボーナス中：スペースで連打してボーナスを稼ごう！ | ESCで終了"
            else:
                help_line = "スペースで連打 → (自動で5秒後に判定) | ESCで終了"
            help_text = font_small.render(help_line, True, (100, 100, 100))
            screen.blit(help_text, ((W - help_text.get_width()) // 2, H - 80))
            
            pygame.display.flip()

    # メイン処理
    def main():
        running = True
        while running:
            show_menu()
            
            # メニュー画面でのキー入力待機
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                        waiting_for_input = False
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:  # Enter
                            waiting_for_input = False
                        elif event.key == K_ESCAPE:  # ESC
                            return False
                
                clock.tick(60)
            
            if running:
                show_countdown(3)
                running = run_game()

    if __name__ == "__main__":
        main()
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def シューティングゲーム():
    #初期化
    pygame.init()

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

    FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語表示用フォントファイルのパス。
    FONT_SIZE = 28  # フォントサイズ,文字の大きさを指定します。
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定したフォントファイルとサイズでフォントオブジェクトを生成します。
    titlefont = pygame.font.Font(FONT_PATH, 50)

    def want_quit(event):
        return (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)


    #ウィンドウ作成
    # ===============================
    # 画面設定
    # ===============================
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    screen = create_display((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("pygame")

    WIDTH, HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
    clock = pygame.time.Clock()

    # ===============================
    # 画像読み込み
    # ===============================
    enemy_img = pygame.image.load("作成されたゲーム/九州情報大学/シューティングゲーム/素材/57.png").convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (80, 80))

    bg_img = pygame.image.load("作成されたゲーム/九州情報大学/シューティングゲーム/素材/14.png").convert()
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

    crosshair_img = pygame.image.load("作成されたゲーム/九州情報大学/シューティングゲーム/素材/50.png").convert_alpha()
    crosshair_img = pygame.transform.scale(crosshair_img, (40, 40))

    # ===============================
    # BGM設定
    # ===============================
    pygame.mixer.music.load("作成されたゲーム/九州情報大学/シューティングゲーム/素材/8.mp3")
    pygame.mixer.music.set_volume(0.4)
    bgm_playing = False

    # ===============================
    # ゲーム変数
    # ===============================
    cross_x = WIDTH // 2
    cross_y = HEIGHT // 2
    cross_speed = 3.5

    score = 0
    hp = 100
    game_result = None

    # ===============================
    # 敵生成
    # ===============================
    def create_enemies(n):
        enemies = []
        for _ in range(n):
            x = random.randint(100, WIDTH - 50)
            y = random.randint(100, HEIGHT - 50)
            enemies.append([x, y])
        return enemies

    enemies = create_enemies(20)
    killed_order = []

    # ===============================
    # リセット処理
    # ===============================
    def reset_game():
        nonlocal enemies, killed_order, score, hp
        nonlocal cross_x, cross_y, game_result, bgm_playing

        enemies = create_enemies(20)
        killed_order = []
        score = 0
        hp = 100

        cross_x = WIDTH // 2
        cross_y = HEIGHT // 2

        game_result = None
        bgm_playing = False
    
    def want_quit(event):
        return (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE)

    # ===============================
    # スタート画面
    # ===============================
    def show_start_screen():
        running=True
        while running:
            screen.fill((80, 208, 255))

            title = titlefont.render("シューティングゲーム", True, (255, 255, 255))
            screen.blit(title, (120, 150))

            text = font.render("スペースを押してゲーム開始！　的を撃ちぬけ！", True, (255, 255, 255))
            screen.blit(text, (110, 350))

            for event in pygame.event.get():
                if want_quit(event):
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return "start"



            pygame.display.update()
            clock.tick(60)

    # ===============================
    # クリア画面
    # ===============================
    def show_clear_screen():
        while True:
            screen.fill((80, 208, 255))

            cleartext = font.render("おめでとう！ゲームクリア！", True, (255, 255, 255))
            screen.blit(cleartext, (200, 200))

            info = font.render("スペースキーで終了", True, (255, 255, 255))
            screen.blit(info, (250, 300))

            for event in pygame.event.get():
                if want_quit(event):
                    return "quit"
                if event.type == KEYDOWN and event.key == K_SPACE:
                    return "end"


            pygame.display.update()
            clock.tick(60)

    # ===============================
    # ゲームオーバー画面
    # ===============================
    def show_gameover_screen():
        while True:
            screen.fill((0, 0, 0))

            over_text = titlefont.render("ゲームオーバー", True, (255, 0, 0))
            screen.blit(over_text, (250, 200))

            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (300, 280))

            info = font.render("スペースキーでリスタートできます", True, (255, 255, 255))
            screen.blit(info, (260, 350))

            for event in pygame.event.get():
                if want_quit(event):
                    return "quit"
                if event.type == KEYDOWN and event.key == K_SPACE:
                    return "retry"



            pygame.display.update()
            clock.tick(60)

    # ===============================
    # メインループ
    # ===============================
    while True:
        act = show_start_screen()   # ← まず代入（これが必須）
        if act == "quit":
            pygame.mixer.music.stop()
            return

        if act != "start":
            continue  # ← これを入れる（start以外ならまたスタート画面へ）
        reset_game()

        running = True

        while running:
            if not bgm_playing:
                pygame.mixer.music.play(-1)
                bgm_playing = True

            clock.tick(60)

            # -------- イベント --------
            for event in pygame.event.get():
                if want_quit(event):
                    pygame.mixer.music.stop()
                    return  # ← ここでシューティングゲーム() を終了

                if event.type == KEYDOWN and event.key == K_SPACE:
                    for i, (ex, ey) in enumerate(enemies):
                        if crosshair_img.get_rect(center=(cross_x, cross_y)).colliderect(
                                enemy_img.get_rect(center=(ex, ey))):
                            score += 10
                            killed_order.append([ex, ey])
                            del enemies[i]
                            break


            # -------- クロスヘア移動 --------
            if enemies:
                target = min(enemies, key=lambda e: math.hypot(e[0]-cross_x, e[1]-cross_y))
                dx, dy = target[0]-cross_x, target[1]-cross_y
                dist = math.hypot(dx, dy)

                if dist != 0:
                    cross_x += dx / dist * cross_speed
                    cross_y += dy / dist * cross_speed

                if dist < 5:
                    hp -= 10
                    killed_order.append(target)
                    enemies.remove(target)

            if len(killed_order) >= 10:
                enemies.append(killed_order.pop(0))

            # -------- 判定 --------
            if score >= 150:
                pygame.mixer.music.stop()
                game_result = "クリア"
                running = False

            if hp <= 0:
                pygame.mixer.music.stop()
                game_result = "ゲームオーバー"
                running = False

            # -------- 描画 --------
            screen.blit(bg_img, (0, 0))
            for ex, ey in enemies:
                screen.blit(enemy_img, enemy_img.get_rect(center=(ex, ey)))

            screen.blit(crosshair_img, crosshair_img.get_rect(center=(cross_x, cross_y)))
            screen.blit(font.render(f"HP: {hp}", True, (200, 0, 0)), (500, 20))
            screen.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (300, 20))
            screen.blit(font.render("シューティングゲーム", True, (0, 0, 0)), (10, 20))

            pygame.display.update()

        # ===== 結果画面 =====
        if game_result == "クリア":
            act = show_clear_screen()
            pygame.mixer.music.stop()
            return

        elif game_result == "ゲームオーバー":
            act = show_gameover_screen()
            if act == "retry":
                continue
            else:  # "quit"
                pygame.mixer.music.stop()
                return





















#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#ゲーム選択関数
def game_select(a):
    global high_score
    pygame.mixer.music.stop()
    click.play() 
    pygame.mouse.set_visible(True)
    if a==1:
        SwitchQuiz()
        
    elif a==2:
        チンチロバトル()

    elif a==3:
        ロボットジャンプ()
    
    elif a==4:
        音楽ゲーム()

    elif a==5:
        時の管理者()

    elif a==6:
        high_score=避けろ(high_score)

    elif a==7:
        OrderRecall()

    elif a==8:
        Quick_Draw()
    
    elif a==9:
        shampoo()
    
    elif a==0:
        シューティングゲーム()







    stop_all_audio()
    pygame.mouse.set_visible(False)
    pygame.mixer.music.play(-1)
    
    



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#セレクト画面
selectscene=0

gazousizex=542
gazousizey=292
gazousizex1=484
gazousizey1=262


jouhou_1 = pygame.transform.smoothscale(jouhou_1, (gazousizex, gazousizey))
jouhou_1_button = jouhou_1.get_rect()
jouhou_2 = pygame.transform.smoothscale(jouhou_2, (gazousizex, gazousizey))
jouhou_2_button = jouhou_2.get_rect()
jouhou_3 = pygame.transform.smoothscale(jouhou_3, (gazousizex, gazousizey))
jouhou_3_button = jouhou_3.get_rect()
jouhou_4 = pygame.transform.smoothscale(jouhou_4, (gazousizex, gazousizey))
jouhou_4_button = jouhou_4.get_rect()

junsin_1 = pygame.transform.smoothscale(junsin_1, (gazousizex1, gazousizey1))
junsin_1_button = junsin_1.get_rect()
junsin_2 = pygame.transform.smoothscale(junsin_2, (gazousizex1, gazousizey1))
junsin_2_button = junsin_2.get_rect()
junsin_3 = pygame.transform.smoothscale(junsin_3, (gazousizex1, gazousizey1))
junsin_3_button = junsin_3.get_rect()
junsin_4 = pygame.transform.smoothscale(junsin_4, (gazousizex1, gazousizey1))
junsin_4_button = junsin_4.get_rect()
junsin_5 = pygame.transform.smoothscale(junsin_5, (gazousizex1, gazousizey1))
junsin_5_button = junsin_5.get_rect()
junsin_6 = pygame.transform.smoothscale(junsin_6, (gazousizex1, gazousizey1))
junsin_6_button = junsin_6.get_rect()

yajirusibotan_left = selectscene_yajirusi.get_rect()
yajirusibotan_right = selectscene_yajirusi1.get_rect()
kasorux=1920/2
kasoruy=1080/2
pygame.mouse.set_visible(False)




#メインループ
runningmain = True    #変数をrunningにTrueを代入
while runningmain:    #変数runningがTrueである間繰り返す（他の変数名、Trueだけでも可）
    
    clock.tick(60)  #フレームレート（fps）を60に制限
    screen.fill((255,255,255)) #背景色(RGB)を描画　これを一番下に持っていき実行すると画面が全部白くなるので注意、背景は最初に持ってこよう
    #イベント取得
    for event in pygame.event.get(): #もし何か（キーが押された、マウスが動いた、クリックされた等）が起きた場合を検知
        if event.type == MOUSEMOTION:
            kasorux,kasoruy = event.pos
        if event.type == pygame.QUIT: #もしウィンドウの×ボタンが押されたなら（フルスクリーンでは表示不可）
            runningmain = False #変数runningにFalseを代入（runningがTrueではないためメインループが終了する）
        if event.type == pygame.KEYDOWN: #もし何かキーが押されたなら
            if event.key == pygame.K_ESCAPE: #押されたキーがもしエスケープキーなら
                runningmain = False  #変数runningにFalseを代入（runningがTrueではないためメインループが終了する）

        if event.type == pygame.MOUSEBUTTONDOWN:# Rectを使ってクリック判定
            if selectscene_sayuu == 0:
                if jouhou_1_button.collidepoint(event.pos):
                    game_select(7)
                if jouhou_2_button.collidepoint(event.pos):
                    game_select(8)
                if jouhou_3_button.collidepoint(event.pos):
                    game_select(9)
                if jouhou_4_button.collidepoint(event.pos):
                    game_select(0)
            elif selectscene_sayuu == 1:
                if junsin_2_button.collidepoint(event.pos):
                    game_select(3)
                if junsin_4_button.collidepoint(event.pos):
                    game_select(4)
                if junsin_5_button.collidepoint(event.pos):
                    game_select(5)
                if junsin_6_button.collidepoint(event.pos):
                    game_select(6)
                if junsin_1_button.collidepoint(event.pos):
                    game_select(1)
                if junsin_3_button.collidepoint(event.pos):
                    game_select(2)
            else:
                click.play() 
                selectscene_sayuu=1
                    

            
            if yajirusibotan_left.collidepoint(event.pos):
                click.play() 
                selectscene_sayuu=1
            if yajirusibotan_right.collidepoint(event.pos):
                click.play() 
                selectscene_sayuu=0
                


    #セレクト画面切り替え
    if selectscene_sayuu == 0:
        screen.blit(selectscene_image, (0, 0))#image配置
        screen.blit(jouhou_1, (373, 264))#image配置
        jouhou_1_button.topleft = (373, 264)
        screen.blit(jouhou_2, (978, 265))#image配置
        jouhou_2_button.topleft = (978, 264)
        screen.blit(jouhou_3, (373, 674))#image配置
        jouhou_3_button.topleft = (373, 674)
        screen.blit(jouhou_4, (977, 674))#image配置
        jouhou_4_button.topleft = (977, 674)
        
        screen.blit(selectscene_yajirusi, (20, 500))#image配置        
        yajirusibotan_left.topleft = (20, 500)

    elif selectscene_sayuu == 1:
        screen.blit(selectscene_image1, (0, 0))#image配置

        screen.blit(junsin_2, (161, 347))#image配置
        junsin_2_button.topleft = (161, 347)
        screen.blit(junsin_4, (701, 347))#image配置
        junsin_4_button.topleft = (701, 347)
        screen.blit(junsin_5, (1239, 349))#image配置
        junsin_5_button.topleft = (1239, 349)
        screen.blit(junsin_6, (161, 713))#image配置
        junsin_6_button.topleft = (161, 713)
        screen.blit(junsin_1, (698, 713))#image配置
        junsin_1_button.topleft = (698, 713)
        screen.blit(junsin_3, (1238, 713))#image配置
        junsin_3_button.topleft = (1238, 713)


        screen.blit(selectscene_yajirusi1, (1750, 500))#image配置        
        yajirusibotan_right.topleft = (1750, 500)

    else:
        
        screen.blit(selectscene_image2, (0, 0))#image配置
    

    screen.blit(image_kasoru,((kasorux-2),(kasoruy-27)))




    

   




    

    #----追加機能を実装、音楽再生等を追加する部分----

    pygame.display.update() #画面更新

#メインループ終了後
pygame.quit() #ウィンドウを閉じる
sys.exit()    #プログラムを終了する
