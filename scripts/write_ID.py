# write_ID.py
# 役割: 取得した選手IDを競技種目ごとのExcelシートに書き込む。
# 変数:
#   - cells: 書き込むセルのリスト
#   - ids: 各競技の選手IDリスト
#   - sheet_name: 書き込む対象のシート名
#   - output_filename: 出力するExcelのファイル名

import os
import openpyxl
from scripts.get_ID import get_player_id

def write_to_excel(input_filename, output_filename, sheet_name, cells, names):
    """
    指定したExcelのシートに選手IDを記入する。

    引数:
        - input_filename: 元となるExcelテンプレートファイル
        - output_filename: 出力するExcelファイル名
        - sheet_name: 書き込むシート名
        - cells: 書き込むセルのリスト
        - names: 書き込む選手IDリスト
    """
    wb = openpyxl.load_workbook(input_filename)

    if sheet_name not in wb.sheetnames:
        raise ValueError(f"シート名 '{sheet_name}' が見つかりません。")

    new_wb = openpyxl.Workbook()
    new_wb.remove(new_wb.active)  # 初期シート削除
    ws_original = wb[sheet_name]
    ws_new = new_wb.create_sheet(title=sheet_name)

    # セルの値をコピー
    for row in ws_original.iter_rows():
        for cell in row:
            ws_new[cell.coordinate] = cell.value

    # 選手IDを書き込む
    for idx, cell in enumerate(sum(cells, [])):  # cells を平坦化
        if idx < len(names):
            ws_new[cell] = names[idx]

    # 出力先ディレクトリを作成（存在しない場合）
    os.makedirs("data_folder", exist_ok=True)
    output_path = os.path.join("data_folder", output_filename)
    new_wb.save(output_path)
    print(f"Excel ファイルを保存しました: {output_path}")

def main():
    """
    メイン処理:
    1. 競技別に選手IDを取得
    2. Excelのシートに選手IDを書き込む
    3. 結果を出力
    """
    csv_file = "test/merged_output.csv"
    cell_config = {
        50: ["B", "I", "P", "W", "AD", "AK", "AR", "AY", "BF", "BM"],
        100: ["B", "J", "Q", "Y", "AF", "AN", "AT", "BH", "BO"],
        200: ["B", "L", "V", "AF", "AP"],
        400: ["B", "P", "AD"],
    }

    events = [
        (stroke, distance)
        for stroke in ["im", "fly", "ba", "br", "fr"]
        for distance in [50, 100, 200, 400]
    ]

    for stroke, distance in events:
        prefixes = cell_config[distance]
        cells = [
            [f"{prefix}{7 + i * 10 + offset}" for offset in [0, -1, 1, -2, 2, -3]]
            for prefix in prefixes
            for i in range(6)
        ]

        ids = get_player_id(csv_file, (stroke, distance), category="mixed")

        if not ids:
            print(f"イベント {stroke}{distance} のIDデータが見つかりません。")
            continue

        output_filename = f"{distance}{stroke}_id.xlsx"
        sheet_name = f"{distance}m"

        write_to_excel("test/テンプレート.xlsx", output_filename, sheet_name, cells, ids)

if __name__ == "__main__":
    main()
