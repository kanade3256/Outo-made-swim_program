from module.csv_utils import read_csv_data
from module.player_utils import create_player_from_row
from module.player_sort_utils import sort_players_by_event, group_and_sort_all_events
from GUI.apps import main as GUI_main

def main():
    
    # CSV を読んで 2次元リストを取得（1行目は読み捨てなどの処理は csv_utils 内で）
    data = read_csv_data("test_data_file/test.csv")
    # print("CSVデータ:", data)  # デバッグ用出力

    # 1行ごとに PlayerData を作って pl_lst に格納
    pl_lst = []
    for n, row in enumerate(data):
        if n == 0:
            continue
        player = create_player_from_row(row)
        pl_lst.append(player)

    # print("Playerリスト:", pl_lst)  # デバッグ用出力

    # ---------------------------
    # 性別ごとに選手を分ける
    # ---------------------------
    male_players = [p for p in pl_lst if p.sex.lower() == "男"]
    female_players = [p for p in pl_lst if p.sex.lower() == "女"]

    # print("男子選手リスト:", male_players)  # デバッグ用出力
    # print("女子選手リスト:", female_players)  # デバッグ用出力


    ########################################################
    # ここから先は、テスト用として作成したのでけしてもよい
    ########################################################

    # # ---------------------------
    # # 男子選手の全イベントをソートして出力
    # # ---------------------------
    # male_sorted_dict = group_and_sort_all_events(male_players, "male")
    # # print("男子ソート結果:", male_sorted_dict)  # デバッグ用出力

    # print("\n=== 男子 の全イベント ソート結果 ===")
    # for (st, dist), sorted_players in male_sorted_dict.items():
    #     print(f"\n--- {st}, {dist} ---")
    #     for rank, player in enumerate(sorted_players, start=1):
    #         time_str = player.times[(st, dist)]
    #         print(f"{rank}位: {player.name} ({time_str})")

    # # ---------------------------
    # # 女子選手の全イベントをソートして出力
    # # ---------------------------
    # female_sorted_dict = group_and_sort_all_events(female_players, "female")
    # # print("女子ソート結果:", female_sorted_dict)  # デバッグ用出力

    # print("\n=== 女子 の全イベント ソート結果 ===")
    # for (st, dist), sorted_players in female_sorted_dict.items():
    #     print(f"\n--- {st}, {dist} ---")
    #     for rank, player in enumerate(sorted_players, start=1):
    #         time_str = player.times[(st, dist)]
    #         print(f"{rank}位: {player.name} ({time_str})")
    

if __name__ == "__main__":
    GUI_main()