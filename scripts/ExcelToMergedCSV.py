# ExcelToMergedCSV.py
# 役割: ExcelファイルをCSVに変換し、それらを統合する。
# 変数:
#   - files: 指定フォルダ内のExcelファイルのリスト
#   - df: 読み込んだExcelデータ
#   - concatenated_df: 統合されたCSVデータ

import os
import pandas as pd

def excel_to_csv(directory_path):
    """
    フォルダ内のすべてのExcelファイルをCSVに変換する。

    引数:
        - directory_path: Excelファイルが保存されたディレクトリのパス
    """
    files = os.listdir(directory_path)

    for filename in files:
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            excel_file_path = os.path.join(directory_path, filename)

            try:
                df = pd.read_excel(excel_file_path, sheet_name="個人エントリー", engine="openpyxl",
                                   skiprows=[0, 1, 2, 3, 4, 5, 6, 8, 9, 10])
                csv_filename = f"{os.path.splitext(filename)[0]}_個人エントリー.csv"
                df.to_csv(os.path.join(directory_path, csv_filename), index=False, encoding="utf-8-sig")
                print(f"'{csv_filename}' に変換されました。")
            except Exception as e:
                print(f"{filename} の処理中にエラーが発生しました: {e}")

def merge_csv_files(directory_path, output_file):
    """
    フォルダ内のCSVファイルを統合する。

    引数:
        - directory_path: CSVファイルが保存されたディレクトリのパス
        - output_file: 統合後の出力ファイルのパス
    """
    csv_files = [f for f in os.listdir(directory_path) if f.endswith(".csv")]
    concatenated_df = pd.DataFrame()

    for file in csv_files:
        file_path = os.path.join(directory_path, file)

        try:
            df = pd.read_csv(file_path, encoding="utf-8-sig")
            if "氏名" not in df.columns:
                print(f"{file} に '氏名' 列が見つからなかったためスキップ")
                continue

            df = df[df["氏名"].notna()]
            if not df.empty:
                concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)
                print(f"{file} から有効なデータを抽出しました。")

        except Exception as e:
            print(f"{file} の処理中にエラーが発生しました: {e}")

    if not concatenated_df.empty:
        concatenated_df["ID"] = range(1, len(concatenated_df) + 1)
        concatenated_df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"結合後のデータを {output_file} に保存しました。")
    else:
        print("有効なデータがありませんでした。")

if __name__ == "__main__":
    """
    メイン処理:
    1. ExcelファイルをCSVに変換
    2. すべてのCSVを統合
    3. 結果を保存
    """
    directory_path = "test_data_file"
    excel_to_csv(directory_path)
    merge_csv_files(directory_path, "merged_output.csv")
