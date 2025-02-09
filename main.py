from module.csv_utils import read_csv_data
from module.player_utils import create_player_from_row

def main():
    file_path = "data_file/test.csv"
    data = read_csv_data(file_path)

    pl_lst = []
    for n, row in enumerate(data):
        # 元のコードにあった「最初の行をスキップ」仕様を再現
        if n == 0:
            continue
        player = create_player_from_row(row)
        pl_lst.append(player)

    print(pl_lst)
    # ここで pl_lst をさらに加工したり、結果を表示・保存するなどの処理を行う

if __name__ == "__main__":
    main()
