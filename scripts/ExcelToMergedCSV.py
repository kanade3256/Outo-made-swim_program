import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
DIRECTORY_PATH = os.getenv("DIRECTORY_PATH")

def delete_existing_csv(directory_path):
    """
    指定フォルダ内のすべてのCSVファイルを削除する。
    """
    files = os.listdir(directory_path)
    for filename in files:
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            os.remove(file_path)
            print(f"削除しました: {filename}")

def excel_to_csv(directory_path):
    """
    フォルダ内のすべてのExcelファイルをCSVに変換する（既存ファイルは上書き）。
    """
    files = os.listdir(directory_path)
    for filename in files:
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            excel_file_path = os.path.join(directory_path, filename)
            try:
                df = pd.read_excel(
                    excel_file_path, sheet_name="個人エントリー", engine="openpyxl",
                    skiprows=[0, 1, 2, 3, 4, 5, 6, 8, 9, 10]
                )
                csv_filename = f"{os.path.splitext(filename)[0]}_個人エントリー.csv"
                csv_filepath = os.path.join(directory_path, csv_filename)
                # 新しいCSVを保存（上書き）
                df.to_csv(csv_filepath, index=False, encoding="utf-8-sig")
                print(f"'{csv_filename}' に変換されました。（最新データに更新）")
            except Exception as e:
                print(f"{filename} の処理中にエラーが発生しました: {e}")

def merge_csv_files(directory_path, output_file):
    """
    フォルダ内のCSVファイルを統合する。
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

def main():
    """
    メイン処理:
    1. フォルダ内の既存CSVを削除
    2. ExcelファイルをCSVに変換
    3. すべてのCSVを統合
    """
    
    # 既存のCSVファイルを削除
    delete_existing_csv(DIRECTORY_PATH)
    
    # ExcelファイルをCSVに変換
    excel_to_csv(DIRECTORY_PATH)
    
    # すべてのCSVを統合（出力先をtestフォルダ内に指定）
    merge_csv_files(DIRECTORY_PATH, os.path.join(DIRECTORY_PATH, "merged_output.csv"))

if __name__ == "__main__":
    main()
