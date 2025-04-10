# csv_utils.py
# 役割: CSVファイルを読み込むユーティリティ関数を提供する。
# 変数:
#   - file_path: 読み込むCSVファイルのパス
#   - data: 読み込んだCSVデータを格納するリスト

import csv
import os
import logging
from typing import List, Union, Dict, Any, Optional

# ロガーの設定
logger = logging.getLogger(__name__)

def read_csv_data(file_path: str) -> List[List[str]]:
    """
    指定したパスのCSVファイルを読み込み、二次元リストとして返す。

    引数:
        - file_path: 読み込むCSVファイルのパス

    戻り値:
        - データを格納したリスト（最初の行をヘッダーとして含む）
        
    例外:
        - FileNotFoundError: ファイルが存在しない場合
        - PermissionError: ファイルを読み取る権限がない場合
        - UnicodeDecodeError: ファイルのエンコーディングが不正な場合
    """
    if not os.path.exists(file_path):
        logger.error(f"CSVファイルが見つかりません: {file_path}")
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
        
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            data = [row for row in csv_reader]
            
            if not data:
                logger.warning(f"CSVファイルが空です: {file_path}")
                return []
                
            logger.info(f"CSVファイルを正常に読み込みました: {file_path}, {len(data)}行")
            return data
    except PermissionError as e:
        logger.error(f"CSVファイルの読み取り権限がありません: {file_path} - {e}")
        raise PermissionError(f"ファイルの読み取り権限がありません: {file_path}")
    except UnicodeDecodeError as e:
        # UTF-8以外のエンコーディングで試行
        encodings = ["utf-8-sig", "shift-jis", "cp932", "euc-jp"]
        for encoding in encodings:
            try:
                with open(file_path, mode="r", encoding=encoding) as file:
                    csv_reader = csv.reader(file)
                    data = [row for row in csv_reader]
                    logger.info(f"CSVファイルを {encoding} エンコーディングで読み込みました: {file_path}")
                    return data
            except UnicodeDecodeError:
                continue
        
        # すべてのエンコーディングが失敗
        logger.error(f"CSVファイルのエンコーディングが不正です: {file_path}")
        raise UnicodeDecodeError("utf-8", b"", 0, 1, f"ファイルのエンコーディングが不正です: {file_path}")
    except Exception as e:
        logger.error(f"CSVファイル読み込み中に予期しないエラーが発生しました: {file_path} - {e}")
        raise

def write_csv_data(file_path: str, data: List[List[Any]], headers: Optional[List[str]] = None) -> bool:
    """
    指定したパスにCSVファイルを書き込む。

    引数:
        - file_path: 書き込み先のCSVファイルパス
        - data: 書き込むデータの二次元リスト
        - headers: CSVヘッダー（省略可能）

    戻り値:
        - 書き込みが成功した場合はTrue、失敗した場合はFalse
        
    例外:
        - PermissionError: ファイルへの書き込み権限がない場合
        - IOError: ファイル書き込み中にエラーが発生した場合
    """
    try:
        # 出力ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
        
        with open(file_path, mode="w", encoding="utf-8", newline="") as file:
            csv_writer = csv.writer(file)
            
            if headers:
                csv_writer.writerow(headers)
                
            csv_writer.writerows(data)
            
        logger.info(f"CSVファイルへの書き込みが完了しました: {file_path}, {len(data)}行")
        return True
    except PermissionError as e:
        logger.error(f"CSVファイルへの書き込み権限がありません: {file_path} - {e}")
        return False
    except IOError as e:
        logger.error(f"CSVファイル書き込み中にIOエラーが発生しました: {file_path} - {e}")
        return False
    except Exception as e:
        logger.error(f"CSVファイル書き込み中に予期しないエラーが発生しました: {file_path} - {e}")
        return False

def read_csv_as_dict(file_path: str) -> List[Dict[str, str]]:
    """
    指定したパスのCSVファイルを読み込み、辞書のリストとして返す。
    各行はヘッダーをキーとした辞書に変換される。

    引数:
        - file_path: 読み込むCSVファイルのパス

    戻り値:
        - 各行をヘッダーをキーとした辞書で表現したリスト
        
    例外:
        - FileNotFoundError: ファイルが存在しない場合
        - PermissionError: ファイルを読み取る権限がない場合 
    """
    if not os.path.exists(file_path):
        logger.error(f"CSVファイルが見つかりません: {file_path}")
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
        
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            data = [dict(row) for row in csv_reader]
            
            logger.info(f"CSVファイルを辞書として正常に読み込みました: {file_path}, {len(data)}行")
            return data
    except PermissionError as e:
        logger.error(f"CSVファイルの読み取り権限がありません: {file_path} - {e}")
        raise PermissionError(f"ファイルの読み取り権限がありません: {file_path}")
    except UnicodeDecodeError:
        # UTF-8以外のエンコーディングで試行
        for encoding in ["utf-8-sig", "shift-jis", "cp932", "euc-jp"]:
            try:
                with open(file_path, mode="r", encoding=encoding) as file:
                    csv_reader = csv.DictReader(file)
                    data = [dict(row) for row in csv_reader]
                    logger.info(f"CSVファイルを {encoding} エンコーディングで辞書として読み込みました: {file_path}")
                    return data
            except UnicodeDecodeError:
                continue
        
        # すべてのエンコーディングが失敗
        logger.error(f"CSVファイルのエンコーディングが不正です: {file_path}")
        raise
    except Exception as e:
        logger.error(f"CSVファイル読み込み中に予期しないエラーが発生しました: {file_path} - {e}")
        raise
