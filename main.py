# main.py
# 役割: 競技種目ごとに選手データを取得し、タイム順にソートしてランキングを出力する。
# 変数:
#   - data: CSVから読み込んだ選手データ
#   - pl_lst: 選手データを格納するリスト
#   - category: 分類 ('male', 'female', 'mixed' のいずれか)
#   - sorted_dict: 競技別にソートされた選手データの辞書

from scripts.ExcelToMergedCSV import main as ExcelToMergedCSV_main
from scripts.write_ID import main as write_to_excel
from scripts.fill_name import main as fill_name
from GUI.apps import main as GUI_main


def main():
    """
    メイン処理:
    1. CSV からプレイヤーデータを取得
    2. 指定されたカテゴリごとに選手をソート
    3. 結果をコンソールに出力
    """
    # 1. Excel ファイルを結合して CSV ファイルを作成
    ExcelToMergedCSV_main()

    # 2. 結果を Excel ファイルに書き込む
    write_to_excel()

    # 3. 選手の名前・フリガナ・学校名・学年を補完する
    fill_name()

if __name__ == "__main__":
    main()
