import os
import pandas as pd
from typing import List, Optional, NoReturn
import logging
from dotenv import load_dotenv
import traceback
from module.send_message import send_slack_message

# ロガーの設定
logger = logging.getLogger(__name__)

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
                    logger.info(f"ファイルを削除しました: {file_path}")
                except PermissionError as e:
                    logger.error(f"ファイルの削除権限がありません: {file_path} - {e}")
                    send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"ファイルの削除権限がありません: {file_path} - {e}")
        return deleted_files
    except FileNotFoundError as e:
        logger.error(f"ディレクトリが存在しません: {directory_path} - {e}")
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"ディレクトリが存在しません: {directory_path} - {e}")
        return deleted_files
    except Exception as e:
        logger.error(f"delete_existing_csvで予期しないエラー: {e}", exc_info=True)
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"delete_existing_csvで予期しないエラー: {e}\n{traceback.format_exc()}")
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
                    df.to_csv(csv_filepath, index=False, encoding="utf-8-sig")
                    converted_files.append(csv_filename)
                    logger.info(f"Excelファイルを変換しました: {excel_file_path} -> {csv_filepath}")
                except ValueError as e:
                    logger.error(f"Excelファイルのシート読み込みエラー: {excel_file_path} - {e}")
                    send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"Excelファイルのシート読み込みエラー: {excel_file_path} - {e}")
                except Exception as e:
                    logger.error(f"Excelファイルの処理エラー: {excel_file_path} - {e}")
                    send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"Excelファイルの処理エラー: {excel_file_path} - {e}\n{traceback.format_exc()}")
        return converted_files
    except FileNotFoundError as e:
        logger.error(f"ディレクトリが存在しません: {directory_path} - {e}")
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"ディレクトリが存在しません: {directory_path} - {e}")
        return converted_files
    except Exception as e:
        logger.error(f"excel_to_csvで予期しないエラー: {e}", exc_info=True)
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"excel_to_csvで予期しないエラー: {e}\n{traceback.format_exc()}")
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
                    continue
                df = df[df["氏名"].notna()]
                if not df.empty:
                    concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)
                    logger.info(f"CSVファイルから有効なデータを抽出: {file_path}")
                    processed_files += 1
                else:
                    logger.info(f"CSVファイルに有効なデータがありません: {file_path}")
            except pd.errors.EmptyDataError as e:
                logger.error(f"CSVファイルが空です: {file_path} - {e}")
                send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"CSVファイルが空です: {file_path} - {e}")
            except Exception as e:
                logger.error(f"CSVファイル処理エラー: {file_path} - {e}")
                send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"CSVファイル処理エラー: {file_path} - {e}\n{traceback.format_exc()}")
        if not concatenated_df.empty:
            try:
                # IDを追加
                concatenated_df["ID"] = range(1, len(concatenated_df) + 1)
                # 出力ディレクトリが存在しない場合は作成
                os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
                concatenated_df.to_csv(output_file, index=False, encoding="utf-8-sig")
                logger.info(f"結合データを保存しました (処理ファイル数: {processed_files}): {output_file}")
                return concatenated_df
            except PermissionError as e:
                logger.error(f"出力ファイルの書き込み権限がありません: {output_file} - {e}")
                send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"出力ファイルの書き込み権限がありません: {output_file} - {e}")
                return None
            except Exception as e:
                logger.error(f"merge_csv_filesの保存処理で予期しないエラー: {e}", exc_info=True)
                send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"merge_csv_filesの保存処理で予期しないエラー: {e}\n{traceback.format_exc()}")
                return None
        else:
            logger.warning("結合可能な有効なデータがありませんでした")
            send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), "結合可能な有効なデータがありませんでした")
            return None
            
    except FileNotFoundError as e:
        logger.error(f"ディレクトリが存在しません: {directory_path} - {e}")
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"ディレクトリが存在しません: {directory_path} - {e}")
        return None
    except Exception as e:
        logger.error(f"merge_csv_filesで予期しないエラー: {e}", exc_info=True)
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"merge_csv_filesで予期しないエラー: {e}\n{traceback.format_exc()}")
        return None

def main(input_folder=None, output_csv=None) -> NoReturn:
    """
    メイン処理:
    1. フォルダ内の既存CSVを削除
    2. ExcelファイルをCSVに変換
    3. すべてのCSVを統合
    戻り値:
        なし
    """
    load_dotenv()
    input_folder = input_folder or os.getenv("INPUT_DATA_FILE")
    output_csv = output_csv or os.path.join(input_folder, os.getenv("MERGED_CSV_DATA_FILE"))
    try:
        if not input_folder:
            logger.error("環境変数 INPUT_DATA_FILE が設定されていません")
            send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), "環境変数 INPUT_DATA_FILE が設定されていません")
            return
        os.makedirs(input_folder, exist_ok=True)
        delete_existing_csv(input_folder)
        excel_to_csv(input_folder)
        merge_csv_files(input_folder, output_csv)
        logger.info(f"すべての処理が完了しました: {input_folder}")
    except Exception as e:
        logger.error(f"ExcelToMergedCSVメイン処理で予期しないエラー: {e}", exc_info=True)
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"ExcelToMergedCSVメイン処理で予期しないエラー: {e}\n{traceback.format_exc()}")

if __name__ == "__main__":
    main()
