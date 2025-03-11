from module.csv_utils import read_csv_data
from module.player_utils import create_player_from_row
from module.player_sort_utils import group_and_sort_all_events


def get_player_id(csv_path, event, category="mixed"):
    """
    CSVファイルからデータを読み込み、全イベントごとに選手のタイムを並び替えた結果から
    指定されたイベント（例: ("fr", 50)）に該当する選手の名前リストを返す。

    :param csv_path: 読み込み対象のCSVファイルのパス
    :param event: イベントを示すタプル (stroke, distance) 例: ("fr", 50)
    :param category: 集計するカテゴリ ("male", "female", "mixed" など)
    :return: 指定イベントに該当する選手の名前リスト
    """
    # CSVからプレイヤーデータの一覧を取得
    data = read_csv_data(csv_path)
    players = []
    for index, row in enumerate(data):
        if index == 0:  # ヘッダー行をスキップ
            continue
        players.append(create_player_from_row(row))

    # カテゴリに応じた全イベントのソート結果を取得
    sorted_dict = group_and_sort_all_events(players, category)

    # 指定のイベントに対応する選手リストを取得（キーが存在しない場合は空リスト）
    sorted_players = sorted_dict.get(event, [])

    # 各選手のidだけを抽出して返す
    return [player.id for player in sorted_players]


def get_player_info_by_id(player_id_list, csv_path):
    """
    指定されたIDリストに対応する選手の名前と性別を取得する。

    :param player_id_list: 検索対象のプレイヤーIDのリスト
    :param csv_path: 読み込み対象のCSVファイルのパス（全選手データが必要）
    :return: 指定IDに該当する選手の (ID, 名前, 性別) のリスト
    """
    data = read_csv_data(csv_path)
    players = {
        create_player_from_row(row).id: create_player_from_row(row) for row in data[1:]
    }  # ヘッダーをスキップ

    result = [
        (pid, players[pid].name, players[pid].sex)
        for pid in player_id_list
        if pid in players
    ]
    return result
