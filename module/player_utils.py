# player_utils.py
# 役割: CSVの行データを解析し、選手データオブジェクトを作成する。
# 変数:
#   - row: CSVの1行分のデータ
#   - player: 解析後のPlayerDataオブジェクト

from module.player_data import PlayerData
from module.event_utils import EVENT_NAMES, parse_event_name

def create_player_from_row(row: list[str]) -> PlayerData:
    """
    CSVの1行 (リスト) から PlayerData オブジェクトを作成し、EVENT_NAMESで定義した
    種目の列を順番にタイムとしてセットして返す。
    
    rowの想定:
      [id, 氏名, ﾌﾘｶﾞﾅ, 学校名, 学年, 性別, 200IM, 200Ba, ... ]

    引数:
        - row: CSVの1行分のリスト

    戻り値:
        - PlayerDataオブジェクト
    """
    # 先頭6列は基本情報
    player = PlayerData(
        id=row[0],
        name=row[1],
        hurigana=row[2].replace("\u3000", " "),
        team=row[3],
        grade=row[4],
        sex=row[5]
    )

    # 7列目 (インデックス6) 以降がタイム情報
    for col_idx, ev_name in enumerate(EVENT_NAMES, start=6):
        if col_idx >= len(row):
            break

        record = row[col_idx].strip()
        if not record:
            continue  # 空の場合はスキップ
        
        stroke, distance = parse_event_name(ev_name)
        player.set_time(stroke, distance, record)

    return player
