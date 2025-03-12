# get_ID.py
# 役割: 競技ごとに選手リストを作成し、選手IDを取得する。
# 変数:
#   - data: CSVから読み込んだ選手データ
#   - players: すべての選手データ
#   - sorted_dict: 競技別にソートされた選手データの辞書
#   - player_id_list: 取得した選手IDのリスト

from module.csv_utils import read_csv_data
from module.player_utils import create_player_from_row
from module.player_sort_utils import group_and_sort_all_events

def get_player_id(csv_path, event, category="mixed"):
    """
    指定したイベントに参加する選手のIDを取得する。

    引数:
        - csv_path: 読み込み対象のCSVファイルのパス
        - event: イベントを示すタプル (stroke, distance) 例: ("fr", 50)
        - category: 集計するカテゴリ ("male", "female", "mixed" など)

    戻り値:
        - 指定イベントに該当する選手のIDリスト
    """
    data = read_csv_data(csv_path)
    players = [create_player_from_row(row) for row in data[1:]]  # ヘッダーをスキップ

    sorted_dict = group_and_sort_all_events(players, category)
    sorted_players = sorted_dict.get(event, [])

    return [player.id for player in sorted_players]

def get_player_info_by_id(player_id_list, csv_path):
    """
    指定されたIDリストに対応する選手の名前と性別を取得する。

    引数:
        - player_id_list: 検索対象のプレイヤーIDのリスト
        - csv_path: 読み込み対象のCSVファイルのパス（全選手データが必要）

    戻り値:
        - 指定IDに該当する選手の (ID, 名前, 性別) のリスト
    """
    data = read_csv_data(csv_path)
    players = {create_player_from_row(row).id: create_player_from_row(row) for row in data[1:]}

    return [(pid, players[pid].name, players[pid].sex) for pid in player_id_list if pid in players]
