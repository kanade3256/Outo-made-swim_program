import sys
from PySide6.QtWidgets import QApplication
from GUI.windows.mainWindow import MainWindow
from GUI.windows.HomeWindow import HomeWindow

def main():
    """ GUI アプリケーションを起動するメイン関数 """
    app = QApplication(sys.argv)
    
    # メインウィンドウの生成
    main_window = MainWindow()
    
    # ホーム画面の生成
    home_page = HomeWindow()
    main_window.setup_pages(home_page)
    home_page.switch_to_drag_drop.connect(main_window.switch_to_drag_drop)
    # DragDropWindowの生成・接続はMainWindow内で行う

    # メインウィンドウを表示
    main_window.show()
    
    sys.exit(app.exec())  # アプリケーションを実行

if __name__ == "__main__":
    main()
