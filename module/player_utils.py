# player_utils.py
# 役割: CSVの行データを解析し、選手データオブジェクトを作成する。
# 変数:
#   - row: CSVの1行分のデータ
#   - player: 解析後のPlayerDataオブジェクト

import logging
import os
import traceback
from module.send_message import send_slack_message
from module.player_data import PlayerData
from module.event_utils import EVENT_NAMES, parse_event_name

def create_player_from_row(row: list[str]) -> PlayerData:
    try:
        player = PlayerData(
            id=row[-1],
            name=row[1],
            hurigana=row[2].replace("\u3000", " "),
            team=row[3],
            grade=row[4],
            sex=row[5]
        )
        for col_idx, ev_name in enumerate(EVENT_NAMES, start=6):
            if col_idx >= len(row):
                break
            record = row[col_idx].strip()
            if not record:
                continue
            stroke, distance = parse_event_name(ev_name)
            player.set_time(stroke, distance, record)
        return player
    except Exception as e:
        logging.error(f"create_player_from_rowでエラー: {e}", exc_info=True)
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"create_player_from_rowでエラー: {e}\n{traceback.format_exc()}")
        raise
