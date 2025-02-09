import csv
from module.player_data import PlayerData, get_possible_events, COMMON_EVENTS, FREESTYLE_EVENTS # 追加

def read_csv(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        data = [row for row in csv_reader]
    return header, data


header, data  = read_csv("data_file/test.csv")
print(data[0])
pl_lst = []

for n, i in enumerate(data):
    if n == 0:
        continue
    else:
        tmp = PlayerData(id=i[0], name=i[1], hurigana=i[2], team=i[3], grade=i[4], sex=i[5])
        pl_lst.append(tmp)
        print(tmp.name)