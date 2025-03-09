# player_sort_utils.py

from collections import defaultdict
from module.player_data import get_possible_events, COMMON_EVENTS
from module.calc_time import parse_time_str

def sort_players_by_event(players, stroke: str, distance: int):
    """
    指定された stroke, distance のイベントについて、
    players をタイムの速い順に並べて返す。
    """
    def key_func(player):
        time_str = player.times.get((stroke, distance), "0")
        return parse_time_str(time_str)

    # "0"も含めて一旦ソートしたいなら valid_players = players でもOK
    # 記録なしを除外したいなら以下のようにフィルタリング
    valid_players = [p for p in players if p.times.get((stroke, distance), "0") != "0"]
    sorted_list = sorted(valid_players, key=key_func)
    return sorted_list


def group_and_sort_all_events(players, gender: str):
    """
    gender に応じた全イベントをソートし、辞書にまとめて返す。
      - gender が "male":   男子のみ対象, IM/fly/ba/br は共通, frは男子距離
      - gender が "female": 女子のみ対象, IM/fly/ba/br は共通, frは女子距離
      - gender が "mixed":  全員対象, IM/fly/ba/br は共通, frは男女合わせた距離
    返り値:
      {
        (stroke, distance): [ソート済み PlayerData ...],
        ...
      }
    """
    # まず対象の選手・対象のイベント一覧を決める
    if gender.lower() == "male":
        target_players = [p for p in players if p.sex.lower() == "男"]
        events = get_possible_events("male")    # { "im": [...], "fly": [...], ... "fr": [50,100,200,400,1500] }
    elif gender.lower() == "female":
        target_players = [p for p in players if p.sex.lower() == "女"]
        events = get_possible_events("female")  # { "im": [...], "fly": [...], ... "fr": [50,100,200,400,800] }
    elif gender.lower() == "mixed":
        # 全選手を混合でランキングする
        target_players = players
        
        # フリー種目だけ男女両方の距離を合わせるため、COMMON_EVENTS を使いつつ 'fr' を再定義する
        # COMMON_EVENTS は player_data.py で定義されている IM/fly/ba/br の距離マップ
        mixed_events = dict(COMMON_EVENTS)  # IM, fly, ba, br は共通

        # 混合用にフリーは [50, 100, 200, 400, 800, 1500] を union として定義
        mixed_events["fr"] = [50, 100, 200, 400, 800, 1500]
        events = mixed_events
    else:
        raise ValueError(f"Invalid gender: {gender}")

    # 種目ごとにソート
    result = {}
    for stroke, distances in events.items():
        for dist in distances:
            sorted_players = sort_players_by_event(target_players, stroke, dist)
            result[(stroke, dist)] = sorted_players

    return result
