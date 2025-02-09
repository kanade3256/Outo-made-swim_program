import csv
import re
from module.player_data import PlayerData, get_possible_events, COMMON_EVENTS, FREESTYLE_EVENTS # 追加

def read_csv(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # 1行目はヘッダ行だが、何も書かれていないので実質読み捨てになる
        data = [row for row in csv_reader]
    return header, data

header, data = read_csv("data_file/test.csv")
print(data[0])  # 1行目(ヘッダor空行)を除いた、最初のデータ行がどう入っているか確認

pl_lst = []

# CSVファイルの列順に対応するイベント名をあらかじめ用意する
# 7列目～21列目 (インデックス6～20) が下記の順番である想定
event_names = [
    "200IM",  "200Ba",  "200Br",  "200Fly", "200Fr",
    "50Ba",   "50Br",   "50Fly",  "50Fr",
    "400IM",  "400Fr",
    "100Ba",  "100Br",  "100Fly", "100Fr"
]

for n, row in enumerate(data):
    # n == 0 の時にスキップしているのは、もともとのコードが
    # 「1行目は何かの都合で飛ばす」という仕様になっているため
    if n == 0:
        continue
    else:
        # 先頭6列は従来通り PlayerData の基本情報をセット
        tmp = PlayerData(
            id=row[0],
            name=row[1],
            hurigana=row[2].replace("\u3000", " "),
            team=row[3],
            grade=row[4],
            sex=row[5]
        )

        # 7列目(インデックス6)以降のタイムを event_names と対応づけて登録
        for col_idx, ev_name in enumerate(event_names, start=6):
            if col_idx < len(row):
                record = row[col_idx].strip()
                if record:  # 空セルでなければパースして登録
                    # 例: "200IM" → 距離=200, 泳法=im
                    match = re.match(r'(\d+)([A-Za-z]+)', ev_name.strip())
                    if match:
                        dist_str, stroke_str = match.groups()
                        dist = int(dist_str)

                        # 泳法の大文字・小文字揺れを吸収しつつ、内部キーに変換
                        stroke_str = stroke_str.capitalize()  # IM, Ba, Br, Fly, Fr など
                        stroke_map = {
                            'Im':  'im',
                            'Ba':  'ba',
                            'Br':  'br',
                            'Fly': 'fly',
                            'Fr':  'fr'
                        }
                        stroke = stroke_map.get(stroke_str)

                        if stroke:
                            tmp.set_time(stroke, dist, record)

        pl_lst.append(tmp)

print(pl_lst)
