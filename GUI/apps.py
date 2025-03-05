import sys
from PySide6.QtWidgets import QApplication
from GUI.windows.mainWindow import MainWindow  # `window/main_window.py` から `MainWindow` をインポート

def main():
    """ GUI アプリケーションを起動するメイン関数 """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())  # アプリケーションを実行
