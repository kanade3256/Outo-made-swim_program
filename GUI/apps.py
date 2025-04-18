import logging
import os
import sys
import traceback
from module.send_message import send_slack_message
from PySide6.QtWidgets import QApplication
from GUI.windows.mainWindow import MainWindow
from GUI.windows.HomeWindow import HomeWindow

def main():
    """ GUI アプリケーションを起動するメイン関数 """
    try:
        app = QApplication(sys.argv)
        main_window = MainWindow()
        home_page = HomeWindow()
        main_window.setup_pages(home_page)
        home_page.switch_to_drag_drop.connect(main_window.switch_to_drag_drop)
        main_window.show()
        sys.exit(app.exec())
    except Exception as e:
        logging.error(f"GUIアプリケーション起動時にエラー: {e}", exc_info=True)
        send_slack_message(os.getenv("APP_NAME", "AquaProgrammer"), f"GUIアプリケーション起動時にエラー: {e}\n{traceback.format_exc()}")
        raise

if __name__ == "__main__":
    main()
