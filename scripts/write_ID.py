# write_ID.py
# 役割: 取得した選手IDを競技種目ごとのExcelシートに書き込む。
# 変数:
#   - cells: 書き込むセルのリスト
#   - ids: 各競技の選手IDリスト
#   - sheet_name: 書き込む対象のシート名
#   - output_filename: 出力するExcelのファイル名

import os
import logging
import openpyxl
import glob
from typing import List, Tuple, Optional, Dict, Any, Union
from scripts.get_ID import get_player_id
from dotenv import load_dotenv

# ロガーの設定
logger = logging.getLogger(__name__)

# 環境変数の読み込み
load_dotenv()
RESULT_DATA_FILE = os.getenv("RESULT_DATA_FILE")
INPUT_DATA_FILE = os.getenv("INPUT_DATA_FILE")
DIRECTORY_PATH = os.getenv("DIRECTORY_PATH", "test/")
MERGED_CSV_DATA_FILE = os.path.join(DIRECTORY_PATH, os.getenv("MERGED_CSV_DATA_FILE"))
TEMPLATE_FILE = os.getenv("TEMPLATE_FILE")  # テンプレートファイルのパス

def write_to_excel(
    input_filename: str, 
    output_filename: str, 
    sheet_name: str, 
    cells: List[List[str]], 
    names: List[str]
) -> bool:
    """
    指定したExcelのシートに選手IDを記入する。

    引数:
        - input_filename: 元となるExcelテンプレートファイル
        - output_filename: 出力するExcelファイル名
        - sheet_name: 書き込むシート名
        - cells: 書き込むセルのリスト
        - names: 書き込む選手IDリスト
        
    戻り値:
        - 処理が成功した場合はTrue、失敗した場合はFalse
        
    例外:
        - FileNotFoundError: 入力ファイルが見つからない場合
        - ValueError: シート名が無効な場合
        - PermissionError: ファイルへのアクセス権限がない場合
    """
    try:
        logger.info(f"Excelファイルを読み込み中: {input_filename}")
        try:
            wb = openpyxl.load_workbook(input_filename)
        except FileNotFoundError as e:
            logger.error(f"テンプレートファイルが見つかりません: {input_filename} - {e}")
            print(f"エラー: テンプレートファイル '{input_filename}' が見つかりません。")
            return False
        except PermissionError as e:
            logger.error(f"テンプレートファイルへのアクセス権限がありません: {input_filename} - {e}")
            print(f"エラー: テンプレートファイル '{input_filename}' へのアクセス権限がありません。")
            return False
        except Exception as e:
            logger.error(f"ファイルの読み込み中に予期しないエラーが発生しました: {input_filename} - {e}")
            print(f"エラー: テンプレートファイルの読み込み中にエラーが発生しました: {e}")
            return False

        if sheet_name not in wb.sheetnames:
            logger.error(f"指定されたシート名が存在しません: '{sheet_name}'")
            print(f"エラー: シート名 '{sheet_name}' が見つかりません。")
            raise ValueError(f"シート名 '{sheet_name}' が見つかりません。")

        # 新しいワークブックを作成
        new_wb = openpyxl.Workbook()
        new_wb.remove(new_wb.active)  # 初期シート削除
        ws_original = wb[sheet_name]
        ws_new = new_wb.create_sheet(title=sheet_name)

        # セルの値をコピー
        logger.debug(f"シート内容をコピー中: {sheet_name}")
        for row in ws_original.iter_rows():
            for cell in row:
                ws_new[cell.coordinate] = cell.value

        # 選手IDを書き込む
        flat_cells = sum(cells, [])  # cells を平坦化
        written_count = 0
        for idx, cell in enumerate(flat_cells):
            if idx < len(names):
                ws_new[cell] = names[idx]
                written_count += 1

        logger.info(f"選手ID {written_count}件 を書き込みました")

        # 出力先ディレクトリを作成（存在しない場合）
        try:
            os.makedirs(RESULT_DATA_FILE, exist_ok=True)
            output_path = os.path.join(RESULT_DATA_FILE, output_filename)
            new_wb.save(output_path)
            logger.info(f"Excelファイルを保存しました: {output_path}")
            print(f"Excel ファイルを保存しました: {output_path}")
            return True
        except PermissionError as e:
            logger.error(f"出力ファイルへの書き込み権限がありません: {output_path} - {e}")
            print(f"エラー: 出力ファイル '{output_path}' への書き込み権限がありません。")
            return False
        except Exception as e:
            logger.error(f"ファイルの保存中にエラーが発生しました: {output_path} - {e}")
            print(f"エラー: ファイルの保存中にエラーが発生しました: {e}")
            return False

    except Exception as e:
        logger.error(f"Excel書き込み処理中に予期しないエラーが発生しました: {e}", exc_info=True)
        print(f"エラー: Excel書き込み処理中に予期しないエラーが発生しました: {e}")
        return False

def clean_output_directory(directory: str, pattern: str = "*.xlsx") -> int:
    """
    指定ディレクトリ内の特定パターンに一致するファイルを削除する。
    
    引数:
        - directory: ファイルを削除するディレクトリ
        - pattern: 削除対象のファイルパターン (デフォルト: *.xlsx)
        
    戻り値:
        - 削除したファイル数
    """
    deleted_count = 0
    try:
        if not os.path.exists(directory):
            logger.warning(f"削除対象ディレクトリが存在しません: {directory}")
            os.makedirs(directory, exist_ok=True)
            return 0
            
        file_pattern = os.path.join(directory, pattern)
        for file_path in glob.glob(file_pattern):
            try:
                os.remove(file_path)
                deleted_count += 1
                logger.debug(f"ファイルを削除しました: {file_path}")
            except PermissionError as e:
                logger.error(f"ファイルの削除権限がありません: {file_path} - {e}")
                print(f"警告: '{os.path.basename(file_path)}' の削除権限がありません")
            except Exception as e:
                logger.error(f"ファイル削除中にエラーが発生しました: {file_path} - {e}")
                
        logger.info(f"{directory} から {deleted_count}個のファイルを削除しました")
        return deleted_count
    except Exception as e:
        logger.error(f"ディレクトリのクリーン処理中にエラーが発生しました: {directory} - {e}")
        return deleted_count

def main() -> None:
    """
    メイン処理:
    1. 競技別に選手IDを取得
    2. Excelのシートに選手IDを書き込む
    3. 結果を出力
    
    戻り値:
        なし
    """
    try:
        # 環境変数の検証
        if not RESULT_DATA_FILE:
            logger.error("環境変数 RESULT_DATA_FILE が設定されていません")
            print("エラー: 環境変数 RESULT_DATA_FILE が設定されていません")
            return
            
        if not TEMPLATE_FILE:
            logger.error("環境変数 TEMPLATE_FILE が設定されていません")
            print("エラー: 環境変数 TEMPLATE_FILE が設定されていません")
            return
            
        if not os.path.exists(TEMPLATE_FILE):
            logger.error(f"テンプレートファイルが見つかりません: {TEMPLATE_FILE}")
            print(f"エラー: テンプレートファイル '{TEMPLATE_FILE}' が見つかりません")
            return
            
        if not MERGED_CSV_DATA_FILE or not os.path.exists(MERGED_CSV_DATA_FILE):
            logger.error(f"マージされたCSVファイルが見つかりません: {MERGED_CSV_DATA_FILE}")
            print(f"エラー: マージされたCSVファイル '{MERGED_CSV_DATA_FILE}' が見つかりません")
            return
            
        # 出力フォルダ内の過去データを削除
        deleted_count = clean_output_directory(RESULT_DATA_FILE)
        print(f"{RESULT_DATA_FILE}内の過去データである.xlsxファイルを{deleted_count}件削除しました。")

        # 各距離のセル設定
        cell_config = {
            50: ["B", "I", "P", "W", "AD", "AK", "AR", "AY", "BF", "BM"],
            100: ["B", "J", "Q", "Y", "AF", "AN", "AT", "BH", "BO"],
            200: ["B", "L", "V", "AF", "AP"],
            400: ["B", "P", "AD"],
        }

        # 全種目の組み合わせを生成
        events = [
            (stroke, distance)
            for stroke in ["im", "fly", "ba", "br", "fr"]
            for distance in [50, 100, 200, 400]
            if distance in cell_config  # 設定がある距離のみ処理
        ]

        successful_events = 0
        failed_events = 0

        # 各種目のIDを取得してExcelに書き込む
        for stroke, distance in events:
            logger.info(f"イベント {stroke}{distance} の処理を開始")
            
            # セルの設定が存在するか確認
            if distance not in cell_config:
                logger.warning(f"距離 {distance}m のセル設定が存在しません")
                continue
                
            prefixes = cell_config[distance]
            cells = [
                [f"{prefix}{7 + i * 10 + offset}" for offset in [0, -1, 1, -2, 2, -3]]
                for prefix in prefixes
                for i in range(6)
            ]

            try:
                # 選手IDを取得
                ids = get_player_id(MERGED_CSV_DATA_FILE, (stroke, distance), category="mixed")
                
                if not ids:
                    logger.warning(f"イベント {stroke}{distance} のIDデータが見つかりません")
                    print(f"イベント {stroke}{distance} のIDデータが見つかりません。")
                    failed_events += 1
                    continue

                output_filename = f"{distance}{stroke}_id.xlsx"
                sheet_name = f"{distance}m"
                
                # IDを書き込み
                success = write_to_excel(TEMPLATE_FILE, output_filename, sheet_name, cells, ids)
                
                if success:
                    successful_events += 1
                    logger.info(f"イベント {stroke}{distance} の処理が成功しました")
                else:
                    failed_events += 1
                    logger.error(f"イベント {stroke}{distance} の処理が失敗しました")
                    
            except FileNotFoundError as e:
                logger.error(f"ファイルが見つかりません: {e}")
                print(f"エラー: ファイルが見つかりません: {e}")
                failed_events += 1
                continue
                
            except ValueError as e:
                logger.error(f"イベント {stroke}{distance} の処理中に値エラーが発生しました: {e}")
                print(f"エラー: イベント {stroke}{distance} の処理中に値エラーが発生しました: {e}")
                failed_events += 1
                continue
                
            except Exception as e:
                logger.error(f"イベント {stroke}{distance} の処理中に予期しないエラーが発生しました: {e}")
                print(f"エラー: イベント {stroke}{distance} の処理中にエラーが発生しました: {e}")
                failed_events += 1
                continue

        # 処理結果のサマリーを出力
        logger.info(f"処理完了: 成功={successful_events}件, 失敗={failed_events}件")
        if successful_events > 0:
            print(f"処理が完了しました。{successful_events}件のイベントを正常に処理しました。")
        if failed_events > 0:
            print(f"警告: {failed_events}件のイベントで処理に失敗しました。")
            
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}", exc_info=True)
        print(f"エラー: 予期しないエラーが発生しました: {e}")

if __name__ == "__main__":
    main()
