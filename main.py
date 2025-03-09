# main.py

from module.csv_utils import read_csv_data
from module.player_utils import create_player_from_row
from module.player_sort_utils import group_and_sort_all_events

def main():
    # CSV からプレイヤーデータの一覧を取得
    data = read_csv_data("test_data_file/test.csv")
    pl_lst = []
    for n, row in enumerate(data):
        if n == 0:
            continue
        pl_lst.append(create_player_from_row(row))

    # -- ここで集計をするときに "male" | "female" | "mixed" を切り替える --
    category = "mixed"  # ここを "male" / "female" / "mixed" で切り替えたり、引数化したりする

    sorted_dict = group_and_sort_all_events(pl_lst, category)
    print(f"\n=== {category} の全イベント ソート結果 ===")

    for (stroke, dist), sorted_players in sorted_dict.items():
        print(f"\n--- {stroke}, {dist} ---")
        for rank, player in enumerate(sorted_players, start=1):
            time_str = player.times.get((stroke, dist), "0")
            print(f"{rank}位: {player.name} ({time_str})")

if __name__ == "__main__":
    main()
