# csv_utils.py
# 役割: CSVファイルを読み込むユーティリティ関数を提供する。
# 変数:
#   - file_path: 読み込むCSVファイルのパス
#   - data: 読み込んだCSVデータを格納するリスト

import csv

def read_csv_data(file_path: str) -> list[list[str]]:
    """
    指定したパスのCSVファイルを読み込み、二次元リストとして返す。

    引数:
        - file_path: 読み込むCSVファイルのパス

    戻り値:
        - データを格納したリスト（ヘッダーは除外）
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)  # ヘッダー行をスキップ
        data = [row for row in csv_reader]
    return data
