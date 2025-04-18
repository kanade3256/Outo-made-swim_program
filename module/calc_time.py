import logging
import os
import traceback
from module.send_message import send_slack_message


def parse_time_str(time_str: str) -> float:
    try:
        time_str = time_str.strip()
        if not time_str or time_str == "0":
            return 999999.9
        if ":" in time_str:
            parts = time_str.split(":")
            if len(parts) == 2:
                minutes_part = parts[0] if parts[0] else "0"
                minutes = float(minutes_part)
                seconds = float(parts[1])
                return minutes * 60 + seconds
            else:
                raise ValueError(f"不正なタイム形式: {time_str}")
        else:
            return float(time_str)
    except Exception as e:
        logging.error(f"parse_time_strでエラー: {e}", exc_info=True)
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"parse_time_strでエラー: {e}\n{traceback.format_exc()}")
        raise

if __name__ == "__main__":
    try:
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
    except Exception as e:
        logging.error(f"__main__テストでエラー: {e}", exc_info=True)
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"calc_time.py __main__テストでエラー: {e}\n{traceback.format_exc()}")