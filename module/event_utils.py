# event_utils.py
# 役割: 競技種目名の解析やイベント情報の管理を行う。
# 変数:
#   - event_name: 解析対象の競技種目名
#   - stroke: 泳法（例: 'fr', 'ba', 'fly'）
#   - distance: 距離（例: 50, 100, 200）

import re

# CSVファイルの列順に対応するイベント名をあらかじめ用意する
# 7列目～21列目(インデックス6～20)がこの順番である想定
EVENT_NAMES = [
    "200IM",  "200Ba",  "200Br",  "200Fly", "200Fr",
    "50Ba",   "50Br",   "50Fly",  "50Fr",
    "400IM",  "400Fr",
    "100Ba",  "100Br",  "100Fly", "100Fr"
]

def parse_event_name(event_name: str) -> tuple[str, int]:
    """
    例: "200IM" -> ("im", 200)
         "50Fr" -> ("fr", 50)
    イベント名の文字列をパースして泳法(stroke)と距離(distance)を返す。

    引数:
        - event_name: イベント名 (例: "200IM")

    戻り値:
        - (泳法, 距離) のタプル
    """
    match = re.match(r'(\d+)([A-Za-z]+)', event_name.strip())
    if not match:
        raise ValueError(f"イベント名 '{event_name}' をパースできません")

    dist_str, stroke_str = match.groups()
    distance = int(dist_str)
    
    # IM, Ba, Br, Fly, Fr -> im, ba, br, fly, fr
    stroke_map = {
        'Im':  'im',
        'Ba':  'ba',
        'Br':  'br',
        'Fly': 'fly',
        'Fr':  'fr'
    }
    # 大文字小文字を揃える
    stroke_str = stroke_str.capitalize()  # IM, Ba, Br, Fly, Fr など

    if stroke_str not in stroke_map:
        raise ValueError(f"未知の泳法 '{stroke_str}' を検出しました")

    stroke = stroke_map[stroke_str]
    return stroke, distance
