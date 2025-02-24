import pandas as pd
import os
import jaconv

# CSVファイルを指定のエンコーディングで読み込む
df = pd.read_csv(
    "",  # ここで変換するファイルのパスを指定
    encoding="utf-8",
)  # 例: UTF-8を指定


# 全角スペースを半角スペースに変換 & 全角カタカナを半角カタカナに変換
def normalize_text(text):
    if isinstance(text, str):
        text = text.replace("\u3000", " ")  # 全角スペースを半角スペースに変換
        text = jaconv.z2h(
            text, kana=True, digit=False, ascii=False
        )  # 全角カタカナを半角に変換
    return text


df = df.applymap(normalize_text)

# 時間の値が入っている複数の列名を指定
column_names = [
    "200IM",
    "200Ba",
    "200Br",
    "200Fly",
    "200Fr",
    "50Ba",
    "50Br",
    "50Fly",
    "50Fr",
    "400IM",
    "400Fr",
    "100Ba",
    "100Br",
    "100Fly",
    "100Fr",
]


# 各列を確認して、タイムフォーマットに変換
def convert_to_time_format(num):
    if pd.isna(num):
        return num
    minutes = int(num // 60)
    seconds = num % 60
    if minutes > 0:
        return f"{minutes}:{seconds:05.2f}"
    else:
        return f"{seconds:.2f}"


for col in column_names:
    if col in df.columns:
        df[col] = df[col].apply(convert_to_time_format)

# 変換結果を指定のエンコーディングで新しいCSVファイルとして保存
df.to_csv(
    "merged_output_converted.csv", index=False, encoding="utf-8"
)  # 例: UTF-8を指定

print("CSVファイルの変換が完了しました。")
