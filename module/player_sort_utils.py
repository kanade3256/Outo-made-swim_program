# player_sort_utils.py

import logging
import os
import traceback
from module.send_message import send_slack_message
from collections import defaultdict
from module.player_data import get_possible_events, COMMON_EVENTS
from module.calc_time import parse_time_str

def sort_players_by_event(players, stroke: str, distance: int):
    try:
        def key_func(player):
            time_str = player.times.get((stroke, distance), "0")
            return parse_time_str(time_str)
        valid_players = [p for p in players if p.times.get((stroke, distance), "0") != "0"]
        sorted_list = sorted(valid_players, key=key_func)
        return sorted_list
    except Exception as e:
        logging.error(f"sort_players_by_eventでエラー: {e}", exc_info=True)
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"sort_players_by_eventでエラー: {e}\n{traceback.format_exc()}")
        raise


def group_and_sort_all_events(players, gender: str):
    try:
        if gender.lower() == "male":
            target_players = [p for p in players if p.sex.lower() == "男"]
            events = get_possible_events("male")
        elif gender.lower() == "female":
            target_players = [p for p in players if p.sex.lower() == "女"]
            events = get_possible_events("female")
        elif gender.lower() == "mixed":
            target_players = players
            mixed_events = dict(COMMON_EVENTS)
            mixed_events["fr"] = [50, 100, 200, 400, 800, 1500]
            events = mixed_events
        else:
            raise ValueError(f"Invalid gender: {gender}")
        result = {}
        for stroke, distances in events.items():
            for dist in distances:
                sorted_players = sort_players_by_event(target_players, stroke, dist)
                result[(stroke, dist)] = sorted_players
        return result
    except Exception as e:
        logging.error(f"group_and_sort_all_eventsでエラー: {e}", exc_info=True)
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"group_and_sort_all_eventsでエラー: {e}\n{traceback.format_exc()}")
        raise
