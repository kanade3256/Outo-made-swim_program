# DataConvert.py
# 役割: CSVデータを正規化し、文字のフォーマット変換やタイムデータの整形を行う。
# 変数:
#   - df: CSVデータを格納するPandasのDataFrame
#   - column_names: タイム変換を適用するカラム名のリスト

import pandas as pd
import os
import jaconv

def normalize_text(text):
    """
    テキストを正規化する（全角スペースを半角に、全角カタカナを半角に変換）。

    引数:
        - text: 変換対象の文字列

    戻り値:
        - 正規化された文字列
    """
    if isinstance(text, str):
        text = text.replace("\u3000", " ")  # 全角スペースを半角スペースに変換
        text = jaconv.z2h(text, kana=True, digit=False, ascii=False)  # 全角カタカナを半角に変換
    return text

def convert_to_time_format(num):
    """
    数値を競泳タイムのフォーマットに変換する。

    引数:
        - num: 数値（例: 220.0）

    戻り値:
        - タイムフォーマットの文字列（例: "2:20.00"）
    """
    if pd.isna(num):
        return num
    minutes = int(num // 100)
    seconds = num % 60
    if minutes > 0:
        return f"{minutes}:{seconds:05.2f}"
    else:
        return f"{seconds:.2f}"

if __name__ == "__main__":
    input_folder = "input_data_folder"
    input_csv = os.path.join(input_folder, "merged_output.csv")
    output_csv = os.path.join(input_folder, "merged_output_converted.csv")
    df = pd.read_csv(input_csv, encoding="utf-8")
    df = df.applymap(normalize_text)
    column_names = ["200IM", "200Ba", "200Br", "200Fly", "200Fr", "50Ba", "50Br", "50Fly", "50Fr", 
                    "400IM", "400Fr", "100Ba", "100Br", "100Fly", "100Fr"]
    for col in column_names:
        if col in df.columns:
            df[col] = df[col].apply(convert_to_time_format)
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print("CSVファイルの変換が完了しました。")
