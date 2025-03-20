import os
import pandas as pd
from typing import List, Optional, NoReturn
import logging
from dotenv import load_dotenv

# ロガーの設定
logger = logging.getLogger(__name__)

load_dotenv()
DIRECTORY_PATH = os.getenv("DIRECTORY_PATH")   

def delete_existing_csv(directory_path: str) -> List[str]:
    """
    指定フォルダ内のすべてのCSVファイルを削除する。
    
    引数:
        directory_path: CSVファイルを削除するディレクトリのパス
        
    戻り値:
        削除したファイル名のリスト
        
    例外:
        FileNotFoundError: ディレクトリが存在しない場合
        PermissionError: ファイルの削除権限がない場合
    """
    deleted_files = []
    try:
        files = os.listdir(directory_path)
        for filename in files:
            if filename.endswith(".csv"):
                file_path = os.path.join(directory_path, filename)
                try:
                    os.remove(file_path)
                    deleted_files.append(filename)
                    print(f"削除しました: {filename}")
                    logger.info(f"ファイルを削除しました: {file_path}")
                except PermissionError as e:
                    logger.error(f"ファイルの削除権限がありません: {file_path} - {e}")
                    print(f"エラー: {filename} の削除権限がありません")
        return deleted_files
    except FileNotFoundError as e:
        logger.error(f"ディレクトリが存在しません: {directory_path} - {e}")
        print(f"エラー: ディレクトリ {directory_path} が見つかりません")
        return deleted_files

def excel_to_csv(directory_path: str) -> List[str]:
    """
    フォルダ内のすべてのExcelファイルをCSVに変換する（既存ファイルは上書き）。
    
    引数:
        directory_path: Excelファイルを検索するディレクトリのパス
        
    戻り値:
        変換に成功したCSVファイル名のリスト
        
    例外:
        FileNotFoundError: ディレクトリまたはExcelファイルが存在しない場合
        ValueError: Excelファイルの読み込みに失敗した場合
    """
    converted_files = []
    try:
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
                    converted_files.append(csv_filename)
                    print(f"'{csv_filename}' に変換されました。（最新データに更新）")
                    logger.info(f"Excelファイルを変換しました: {excel_file_path} -> {csv_filepath}")
                except ValueError as e:
                    logger.error(f"Excelファイルのシート読み込みエラー: {excel_file_path} - {e}")
                    print(f"{filename} の処理中にエラーが発生しました: {e}")
                except Exception as e:
                    logger.error(f"Excelファイルの処理エラー: {excel_file_path} - {e}")
                    print(f"{filename} の処理中にエラーが発生しました: {e}")
        return converted_files
    except FileNotFoundError as e:
        logger.error(f"ディレクトリが存在しません: {directory_path} - {e}")
        print(f"エラー: ディレクトリ {directory_path} が見つかりません")
        return converted_files

def merge_csv_files(directory_path: str, output_file: str) -> Optional[pd.DataFrame]:
    """
    フォルダ内のCSVファイルを統合する。
    
    引数:
        directory_path: CSVファイルを検索するディレクトリのパス
        output_file: 結合したデータを保存する出力ファイルパス
        
    戻り値:
        結合したDataFrame、有効なデータがない場合はNone
        
    例外:
        FileNotFoundError: ディレクトリが存在しない場合
        PermissionError: 出力ファイルの書き込み権限がない場合
    """
    try:
        csv_files = [f for f in os.listdir(directory_path) if f.endswith(".csv")]
        concatenated_df = pd.DataFrame()
        processed_files = 0
        
        for file in csv_files:
            file_path = os.path.join(directory_path, file)
            try:
                df = pd.read_csv(file_path, encoding="utf-8-sig")
                if "氏名" not in df.columns:
                    logger.warning(f"CSVファイルに氏名列がありません: {file_path}")
                    print(f"{file} に '氏名' 列が見つからなかったためスキップ")
                    continue
                df = df[df["氏名"].notna()]
                if not df.empty:
                    concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)
                    print(f"{file} から有効なデータを抽出しました。")
                    logger.info(f"CSVファイルから有効なデータを抽出: {file_path}")
                    processed_files += 1
                else:
                    logger.info(f"CSVファイルに有効なデータがありません: {file_path}")
            except pd.errors.EmptyDataError as e:
                logger.error(f"CSVファイルが空です: {file_path} - {e}")
                print(f"{file} は空のファイルです: {e}")
            except Exception as e:
                logger.error(f"CSVファイル処理エラー: {file_path} - {e}")
                print(f"{file} の処理中にエラーが発生しました: {e}")

        if not concatenated_df.empty:
            try:
                # IDを追加
                concatenated_df["ID"] = range(1, len(concatenated_df) + 1)
                # 出力ディレクトリが存在しない場合は作成
                os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
                concatenated_df.to_csv(output_file, index=False, encoding="utf-8-sig")
                print(f"結合後のデータを {output_file} に保存しました。")
                logger.info(f"結合データを保存しました (処理ファイル数: {processed_files}): {output_file}")
                return concatenated_df
            except PermissionError as e:
                logger.error(f"出力ファイルの書き込み権限がありません: {output_file} - {e}")
                print(f"エラー: {output_file} への書き込み権限がありません")
                return None
        else:
            logger.warning("結合可能な有効なデータがありませんでした")
            print("有効なデータがありませんでした。")
            return None
            
    except FileNotFoundError as e:
        logger.error(f"ディレクトリが存在しません: {directory_path} - {e}")
        print(f"エラー: ディレクトリ {directory_path} が見つかりません")
        return None

def main() -> NoReturn:
    """
    メイン処理:
    1. フォルダ内の既存CSVを削除
    2. ExcelファイルをCSVに変換
    3. すべてのCSVを統合
    
    戻り値:
        なし
    """
    try:
        if not DIRECTORY_PATH:
            logger.error("環境変数 DIRECTORY_PATH が設定されていません")
            print("エラー: 環境変数 DIRECTORY_PATH が設定されていません")
            return
            
        # 既存のCSVファイルを削除
        delete_existing_csv(DIRECTORY_PATH)
        
        # ExcelファイルをCSVに変換
        excel_to_csv(DIRECTORY_PATH)
        
        # すべてのCSVを統合（出力先を指定）
        merge_csv_files(DIRECTORY_PATH, os.path.join(DIRECTORY_PATH, "merged_output.csv"))
        
        logger.info(f"すべての処理が完了しました: {DIRECTORY_PATH}")
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}", exc_info=True)
        print(f"予期しないエラーが発生しました: {e}")

if __name__ == "__main__":
    main()
