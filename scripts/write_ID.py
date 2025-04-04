# write_ID.py
# 役割: 取得した選手IDを競技種目ごとのExcelシートに書き込む。
# 変数:
#   - cells: 書き込むセルのリスト（各グループはコース1～6に対応した順番である前提）
#   - names: 各競技の選手名（ID）のリスト（早い順＝先頭が最速）
#   - sheet_name: 書き込む対象のシート名
#   - output_filename: 出力するExcelのファイル名

import os
import logging
import openpyxl
import glob
from typing import List, Tuple, Optional, Dict, Any, Union
from scripts.get_ID import get_player_id


def partition_names(names):
    """
    名前リスト（早い順）から、最終組を必ず６名にするため、
    まずリストを反転（＝シート上で上が遅い、下が速い）し、
    余り（r = len % 6）があればそれを1組目（上側）に、
    残りを6名ずつのグループに分割する。
    """
    # 入力は早い順なので反転して遅い順にする
    names_rev = names[::-1]
    total = len(names_rev)
    r = total % 6
    groups = []
    start = 0
    if r != 0:
        groups.append(names_rev[:r])
        start = r
    while start < total:
        groups.append(names_rev[start : start + 6])
        start += 6
    return groups


def assign_group(group):
    """
    各グループ内で、中心から埋めるように名前を配置する。
    各グループは最終的に６コース（上からコース1～6）に対応するリストを返す。
    割り当てパターン（速い順に並べた場合のコース割り当て）は：
      最速 → コース4
      2番目 → コース3
      3番目 → コース5
      4番目 → コース2
      5番目 → コース6
      6番目 → コース1
    ※グループの人数が6未満の場合は、パターンの先頭分だけ割り当て、残りは空文字列とする。
    """
    pattern = [4, 3, 5, 2, 6, 1]  # この順番で割り当てる（コース番号）
    # まずグループ内を速い順にする（降順）
    sorted_group = group[::-1]
    # 結果はコース1～6順（インデックス0～5）に対応
    result = ["" for _ in range(6)]
    for i, name in enumerate(sorted_group):
        if i < len(pattern):
            course = pattern[i]
            result[course - 1] = name
    return result


def write_to_excel(input_filename, output_filename, sheet_name, cells, names):
    wb = openpyxl.load_workbook(input_filename)

    if sheet_name not in wb.sheetnames:
        logger.error(f"指定されたシート名が存在しません: '{sheet_name}'")
        print(f"エラー: シート名 '{sheet_name}' が見つかりません。")
        raise ValueError(f"シート名 '{sheet_name}' が見つかりません。")

        # 新しいワークブックを作成
        new_wb = openpyxl.Workbook()
        new_wb.remove(new_wb.active)  # 初期シート削除
        ws_original = wb[sheet_name]
        ws_new = new_wb.create_sheet(title=sheet_name)

    # テンプレートシートのセル内容をコピー
    for row in ws_original.iter_rows():
        for cell in row:
            ws_new[cell.coordinate] = cell.value

    print("入力名前リスト（早い順）の最初の20件:", names[:20])

    # グループ分け（シート上の上からは遅い人、最終組はフルの6名で速い人）
    groups = partition_names(names)
    print("グループごとの人数:", [len(g) for g in groups])

    # 各グループについて、中心から埋めるように再配置（最終結果はコース1～6の順）
    assigned_groups = [assign_group(group) for group in groups]
    # ここで assigned_groups[0] は1組目（上側、人数が余り分）、最後のグループは最速全員

    print("各グループ再配置後（コース1～6順）の内容:")
    for idx, grp in enumerate(assigned_groups, start=1):
        print(f"組 {idx}: {grp}")

    # 修正: セルの位置を3行上にするため、開始行番号を 7 から 4 に変更
    # cells は各グループに対応するセルリスト（各リストはコース1～6の順とする）
    for cell_group, name_group in zip(cells, assigned_groups):
        for cell, name in zip(cell_group, name_group):
            ws_new[cell] = name

    os.makedirs("data_folder", exist_ok=True)
    output_path = os.path.join("data_folder", output_filename)
    new_wb.save(output_path)
    print(f"Excel ファイルを保存しました: {output_path}")


def main():
    """
    メイン処理:
    1. 競技別に選手IDを取得（ここでは名前リスト）
    2. Excel のシートに選手IDを書き込む
    3. 結果を出力
    """
    csv_file = "test/merged_output.csv"
    cell_config = {
        50: ["B", "I", "P", "W", "AD", "AK", "AR", "AY", "BF", "BM"],
        100: ["B", "J", "Q", "Y", "AF", "AN", "AT", "BH", "BO"],
        200: ["B", "L", "V", "AF", "AP"],
        400: ["B", "P", "AD"],
    }

    # 全種目の組み合わせを生成
    events = [
        (stroke, distance)
        for stroke in ["im", "fly", "ba", "br", "fr"]
        for distance in [50, 100, 200, 400]
        if distance in cell_config  # 設定がある距離のみ処理
    ]

    for stroke, distance in events:
        prefixes = cell_config[distance]
        # セルのリストを、各グループ（コース1～6）に対応するよう作成
        # 修正: 各セルの行番号の開始位置を 7 から 4 に変更
        cells = [
            [f"{prefix}{4 + i * 10 + offset}" for offset in range(6)]
            for prefix in prefixes
            for i in range(6)
        ]

        names = get_player_id(csv_file, (stroke, distance), category="mixed")
        if not names:
            print(f"イベント {stroke}{distance} のIDデータが見つかりません。")
            continue

        output_filename = f"{distance}{stroke}_id.xlsx"
        sheet_name = f"{distance}m"

        write_to_excel(
            "test/テンプレート.xlsx", output_filename, sheet_name, cells, names
        )


if __name__ == "__main__":
    main()
