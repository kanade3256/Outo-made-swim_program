# main.py
# 役割: 競技種目ごとに選手データを取得し、タイム順にソートしてランキングを出力する。
# 変数:
#   - data: CSVから読み込んだ選手データ
#   - pl_lst: 選手データを格納するリスト
#   - category: 分類 ('male', 'female', 'mixed' のいずれか)
#   - sorted_dict: 競技別にソートされた選手データの辞書

from module.csv_utils import read_csv_data
from module.player_utils import create_player_from_row
from module.player_sort_utils import group_and_sort_all_events

def main():
    """
    メイン処理:
    1. CSV からプレイヤーデータを取得
    2. 指定されたカテゴリごとに選手をソート
    3. 結果をコンソールに出力
    """
    # CSV からプレイヤーデータの一覧を取得
    data = read_csv_data("test_data_file/test.csv")
    pl_lst = []
    for n, row in enumerate(data):
        if n == 0:
            continue
        pl_lst.append(create_player_from_row(row))

    # 集計カテゴリの設定
    category = "mixed"  # "male" / "female" / "mixed" を指定可能

    sorted_dict = group_and_sort_all_events(pl_lst, category)
    print(f"\n=== {category} の全イベント ソート結果 ===")

    for (stroke, dist), sorted_players in sorted_dict.items():
        print(f"\n--- {stroke}, {dist} ---")
        for rank, player in enumerate(sorted_players, start=1):
            time_str = player.times.get((stroke, dist), "0")
            print(f"{rank}位: {player.name} ({time_str})")

if __name__ == "__main__":
    main()
