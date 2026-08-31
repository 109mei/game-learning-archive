# coding: utf-8
"""
35_exception_io_module_example.py

このスクリプトでは、例外処理（try/except）、ファイル入出力、そして外部モジュールの活用
（math、random、datetime）を組み合わせた基本例を示します。ファイルが存在しない場合の
例外を捕捉し、新しいファイルを作成する方法や、標準モジュールを用いた計算や乱数生成、
現在時刻の取得を行っています。各行にコメントを付けて動作を説明しています。
"""

import math  # mathモジュールを読み込んで数学関数を使用できるようにします
import random  # randomモジュールを読み込んで乱数を生成できるようにします
import datetime  # datetimeモジュールを読み込んで日付と時刻を扱います

# ---------- ファイルの読み込みと例外処理 ----------
file_content = ""  # 読み込んだ内容を保存する変数を初期化します
try:  # ファイル読み込みを試行します
    with open("example.txt", "r", encoding="utf-8") as f:  # 読み込みモードでファイルを開きます
        file_content = f.read()  # ファイルの内容を読み込みます
except FileNotFoundError:  # ファイルが存在しない場合の例外を捕捉します
    file_content = "ファイルが見つかりませんでした。新しく作成します。"  # 代替メッセージを設定します

print("読み込んだ内容:")  # ファイル読み込み結果のヘッダーを表示します
print(file_content)  # ファイルの内容または代替メッセージを表示します

# ---------- ファイルの書き込み ----------
output_message = "これは35のコードの処理でファイルに保存されたメッセージです。消してかまいません"  # 保存するテキストを定義します
with open("output.txt", "w", encoding="utf-8") as out:  # 書き込みモードでファイルを開きます
    out.write(output_message)  # テキストをファイルに書き込みます
print("output.txt にメッセージを書き込みました。")  # 書き込み完了を知らせます

# ---------- math モジュールの使用 ----------
value = 16  # 平方根を求める値を定義します
sqrt_val = math.sqrt(value)  # math.sqrt()を使って平方根を計算します
print(f"{value} の平方根は {sqrt_val}")  # 計算結果を表示します

# ---------- random モジュールの使用 ----------
rand_val = random.random()  # 0以上1未満の乱数を生成します
print(f"生成された乱数: {rand_val}")  # 生成された乱数を表示します

# ---------- datetime モジュールの使用 ----------
current_time = datetime.datetime.now()  # 現在の日時を取得します
print(f"現在の日時: {current_time}")  # 現在の日時を表示します