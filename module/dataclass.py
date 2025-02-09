from dataclasses import dataclass, field
from typing import Dict, Tuple

# --- 1. 種目定義 ---

# フリー以外の種目
#    IM: 100, 200, 400
#    fly, ba, br: 50, 100, 200
COMMON_EVENTS = {
    "im":   [100, 200, 400],
    "fly":  [50, 100, 200],
    "ba":   [50, 100, 200],
    "br":   [50, 100, 200],
}

# フリー種目は男女で距離が変わる
FREESTYLE_EVENTS = {
    "male":   [50, 100, 200, 400, 1500],
    "female": [50, 100, 200, 400, 800],
}

def get_possible_events(gender: str) -> Dict[str, list[int]]:
    """
    性別(gender)に応じて、泳法 -> [距離一覧] を返す。
    """
    # フリー以外（IM, fly, ba, br）は共通
    possible = dict(COMMON_EVENTS)  # コピー
    # フリー種目は性別で距離が異なる
    if gender == "male":
        possible["fr"] = FREESTYLE_EVENTS["male"]
    else:
        possible["fr"] = FREESTYLE_EVENTS["female"]
    return possible


# --- 2. 選手データクラス ---

@dataclass
class PlayerData:
    id: int
    name: str
    hurigana: str
    team: str
    grade: int
    sex: str

    # (泳法, 距離) -> 記録  を保持する辞書
    # 初期化時に全種目のデフォルト値 "0" をセットする
    times: Dict[Tuple[str, int], str] = field(default_factory=dict)

    def __post_init__(self):
        # 性別に応じた可能な種目を取得
        events = get_possible_events(self.sex.lower())
        # (泳法, 距離) をキーに、タイムをデフォルト "0" で初期化
        for stroke, distances in events.items():
            for dist in distances:
                self.times[(stroke, dist)] = "0"

    def set_time(self, stroke: str, distance: int, record: str) -> None:
        """
        選手の種目 (stroke, distance) に対してタイムを登録する。
        """
        key = (stroke, distance)
        if key not in self.times:
            raise ValueError(f"この選手の種目に存在しない (泳法: {stroke}, 距離: {distance}) です。")
        self.times[key] = record


# --- 3. 使い方 ---

if __name__ == "__main__":
    # 例: 女性選手
    player_f = PlayerData(
        id=1, name="田中花子", hurigana="たなかはなこ", team="A", grade=3, sex="female"
    )
    # IM200 のタイムを更新
    player_f.set_time("im", 200, "2:05.3")
    # 女子フリーなので 800m がある
    player_f.set_time("fr", 800, "9:12.5")

    print(f"{player_f.name} のIM200タイム: {player_f.times[('im', 200)]}")
    print(f"{player_f.name} のFR800タイム: {player_f.times[('fr', 800)]}")
    # 男子向けの 1500m はキーがないのでエラーになる

    # 例: 男性選手
    player_m = PlayerData(
        id=2, name="佐藤太郎", hurigana="さとうたろう", team="B", grade=2, sex="male"
    )
    # 男子フリーなので 1500m がある
    player_m.set_time("fr", 1500, "16:45.8")

    # print(f"{player_m.name} のFR1500タイム: {player_m.times[('fr', 1500)]}")
    print(player_m)