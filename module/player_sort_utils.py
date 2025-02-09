from collections import defaultdict
from module.player_data import get_possible_events
from module.calc_time import parse_time_str

def sort_players_by_event(players, stroke: str, distance: int):
    """
    指定された stroke, distance のイベントについて、
    players をタイムの速い順に並べて返す。
    """
    def key_func(player):
        # PlayerData.times[(stroke, distance)] は文字列タイム
        time_str = player.times.get((stroke, distance), "0")
        return parse_time_str(time_str)

    # タイムが登録されていない（'0'）選手も含めてソートしたい場合はそのまま
    # 登録されている選手だけ絞る場合は filter を使う
    valid_players = [p for p in players if p.times.get((stroke, distance), "0") != "0"]
    sorted_list = sorted(valid_players, key=key_func)

    return sorted_list

def group_and_sort_all_events(players, gender: str):
    """
    gender に応じた全イベント (IM, fly, ba, br, fr + 距離) を取得し、
    各イベントごとにタイム順にソートしたリストをまとめた辞書を返す。

    返り値のイメージ:
      {
        ("im", 100): [PlayerDataリスト (タイム順)],
        ("im", 200): [...],
        ...
        ("fr", 50): [...]
      }
    """
    result = {}
    # 性別を元にイベント一覧を取得
    events = get_possible_events(gender)  # -> {'im': [100, 200, 400], 'fly': [50,100,200], ... }
    for stroke, distances in events.items():
        for dist in distances:
            sorted_players = sort_players_by_event(players, stroke, dist)
            result[(stroke, dist)] = sorted_players
    return result

