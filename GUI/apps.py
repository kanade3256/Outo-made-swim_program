# apps.py
import sys
from PySide6.QtWidgets import QApplication
from GUI.windows.main_window import MainWindow

def main():
    """GUIアプリケーションを起動するメイン関数"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
