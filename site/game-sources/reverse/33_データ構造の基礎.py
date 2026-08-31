# coding: utf-8
"""
33_list_dict_example.py

このスクリプトでは、Python のデータ構造であるリストと辞書の基本的な使い方を紹介します。
リストに格納された数値の合計を求める例と、辞書に格納された名前とスコアを反復処理する
例を示します。各行にコメントを付け、データ構造の操作方法が理解しやすいようにしています。
"""

# ---------- リストの例 ----------
numbers = [1, 2, 3, 4, 5]  # 整数を含むリストを定義します
sum_numbers = 0  # 合計を保持する変数を初期化します
for num in numbers:  # リストnumbersの各要素を順に取り出します
    sum_numbers += num  # numをsum_numbersに加算して合計を更新します

print("リストの要素:", numbers)  # リストの内容を表示します
print("要素の合計:", sum_numbers)  # 計算した合計を表示します

# ---------- 辞書の例 ----------
scores = {"Alice": 95, "Bob": 80, "Charlie": 70}  # 名前をキー、スコアを値とする辞書を定義します

print("\n辞書の内容:")  # 改行を入れて見やすくします
for name, score in scores.items():  # items()でキーと値のペアを順に取り出します
    print(f"{name} のスコアは {score}")  # f文字列で名前とスコアを表示します