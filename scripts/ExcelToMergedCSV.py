import os
import pandas as pd


def excel_to_csv(directory_path):
    # 指定フォルダ内のファイル一覧を取得
    files = os.listdir(directory_path)

    for filename in files:
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            excel_file_path = os.path.join(directory_path, filename)

            try:
                # "個人エントリー" シートからデータを取得し、不要な行をスキップ
                df = pd.read_excel(
                    excel_file_path,
                    sheet_name="個人エントリー",
                    engine="openpyxl",
                    skiprows=[0, 1, 2, 3, 4, 5, 6, 8, 9, 10],  # スキップする行
                )

                # 出力CSVファイルのパスを生成
                csv_filename = f"{os.path.splitext(filename)[0]}_個人エントリー.csv"
                csv_file_path = os.path.join(directory_path, csv_filename)

                # CSVに書き出し
                df.to_csv(csv_file_path, index=False, encoding="utf-8-sig")
                print(f"'{csv_file_path}' に変換されました。")

            except Exception as e:
                print(f"{filename} の処理中にエラーが発生しました: {e}")


def merge_csv_files(directory_path, output_file):
    # 指定ディレクトリ内のCSVファイル一覧を取得
    csv_files = [f for f in os.listdir(directory_path) if f.endswith(".csv")]
    concatenated_df = pd.DataFrame()

    for file in csv_files:
        file_path = os.path.join(directory_path, file)

        try:
            df = pd.read_csv(file_path, encoding="utf-8-sig")

            # 氏名列が存在しない場合はスキップ
            if "氏名" not in df.columns:
                print(f"{file} に '氏名' 列が見つからなかったためスキップ")
                continue

            # 氏名が NaN でない行のみを抽出
            df = df[df["氏名"].notna()]

            # 有効なデータがある場合のみ結合
            if not df.empty:
                concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)
                print(f"{file} から有効なデータを抽出しました。")

        except Exception as e:
            print(f"{file} の処理中にエラーが発生しました: {e}")

    # 結果を保存
    if not concatenated_df.empty:
        concatenated_df["ID"] = range(1, len(concatenated_df) + 1)
        concatenated_df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"結合後のデータを {output_file} に保存しました。")
    else:
        print("有効なデータがありませんでした。")


# 使用例
if __name__ == "__main__":
    directory_path = "test_file2"  # Excelファイルが存在するディレクトリのパスを指定
    excel_to_csv(directory_path)  # フォルダ内のすべてのエクセルファイルを処理
    output_file = "merged_output.csv"  # 出力ファイル名を指定
    merge_csv_files(directory_path, output_file)
