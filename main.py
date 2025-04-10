# main.py
# 役割: 競技種目ごとに選手データを取得し、タイム順にソートしてランキングを出力する。
# 変数:
#   - data: CSVから読み込んだ選手データ
#   - pl_lst: 選手データを格納するリスト
#   - category: 分類 ('male', 'female', 'mixed' のいずれか)
#   - sorted_dict: 競技別にソートされた選手データの辞書

from typing import NoReturn
import os
import logging
import traceback
from scripts.ExcelToMergedCSV import main as ExcelToMergedCSV_main
from scripts.write_ID import main as write_to_excel
from scripts.fill_name import main as fill_name
from GUI.apps import main as GUI_main

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main() -> NoReturn:
    """
    メイン処理:
    1. CSV からプレイヤーデータを取得
    2. 指定されたカテゴリごとに選手をソート
    3. 結果をコンソールに出力
    
    戻り値:
        NoReturn: この関数は値を返しません
    
    例外:
        Exception: 処理中に発生した例外はログに記録され、処理を続行します
    """
    try:
        # 1. Excel ファイルを結合して CSV ファイルを作成
        logger.info("Excelファイルの変換と結合を開始します")
        ExcelToMergedCSV_main()
        
        # 2. 結果を Excel ファイルに書き込む
        logger.info("IDデータの書き込みを開始します")
        write_to_excel()
        
        # 3. 選手の名前・フリガナ・学校名・学年を補完する
        # 現在コメントアウトされているが、必要に応じて有効化
        logger.info("選手情報の補完を開始します")
        fill_name()
        
        logger.info("処理が正常に完了しました")
        return True
    except FileNotFoundError as e:
        logger.error(f"ファイルが見つかりません: {e}")
        logger.error(traceback.format_exc())
        print(f"エラー: ファイルが見つかりません。詳細: {e}")
        raise
    except PermissionError as e:
        logger.error(f"ファイルへのアクセス権限がありません: {e}")
        logger.error(traceback.format_exc())
        print(f"エラー: ファイルへのアクセス権限がありません。詳細: {e}")
        raise
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}")
        logger.error(traceback.format_exc())
        print(f"予期しないエラーが発生しました。詳細: {e}")
        print("ログファイル(app.log)を確認してください")
        raise

if __name__ == "__main__":
    GUI_main()
    # main()
