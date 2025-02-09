import re

def parse_time_str(time_str: str) -> float:
    """
    '1:23.45' などのタイム文字列を秒数(float)に変換して返す。
    '0' や '' の場合は非常に大きな値を返すなどで「未登録・無効」を表現してもよい。
    
    例
      "1:23.45" → 83.45
      "58.12"   → 58.12
    """
    time_str = time_str.strip()
    # print(time_str)
    if not time_str or time_str == "0":
        # タイムが無い場合、ソート時に最下位になるように大きな値を返す
        return 999999.9
    
    # 分:秒.ミリ 形式か、秒.ミリ形式かを判断
    # - 分付き: M:SS.xx (例: "1:23.45")
    # - 分なし: SS.xx   (例: "58.12")
    if ":" in time_str:
        # 分:秒.ミリ の形式
        parts = time_str.split(":")
        if len(parts) == 2:
            # parts[0] = 分, parts[1] = 秒.ミリ
            minutes_part = parts[0] if parts[0] else "0"
            minutes = float(minutes_part)
            seconds = float(parts[1])
            return minutes * 60 + seconds
        else:
            raise ValueError(f"不正なタイム形式: {time_str}")
    else:
        # 秒.ミリ 形式
        return float(time_str)

if __name__ == "__main__":
    print(parse_time_str("1:23.45"))  # 83.45
    print(parse_time_str("58.12"))    # 58.12
    print(parse_time_str("0"))        # 999999.9
    print(parse_time_str(""))         # 999999.9
    print(parse_time_str("1:23"))     # ValueError
    print(parse_time_str("1:23:45"))  # ValueError
    print(parse_time_str("1:23."))    # ValueError
    print(parse_time_str("1:23.45.6"))  # ValueError
    print(parse_time_str("1:23.45.6"))  # ValueError
    print(parse_time_str("1:23.45.6"))  # ValueError