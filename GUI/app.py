from PySide6.QtWidgets import QApplication
from GUI.windows.main_window import MainWindow

def main():
    """ GUIアプリケーションを起動するメイン関数 """
    window = MainWindow()
    window.show()
