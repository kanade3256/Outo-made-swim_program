import csv

def read_csv_data(file_path: str) -> list[list[str]]:
    """
    指定したパスのCSVファイルを読み込み、二次元リストとして返す。
    先頭行(header)は読み捨てる想定。
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        # ヘッダ行を読み捨て
        next(csv_reader, None)
        data = [row for row in csv_reader]
    return data
