import sys
from PySide6.QtWidgets import QApplication
from GUI.windows.mainWindow import MainWindow
from GUI.windows.HomeWindow import HomeWindow
from GUI.windows.DragDropWindow import DragDropWindow

def main():
    """ GUI アプリケーションを起動するメイン関数 """
    app = QApplication(sys.argv)
    
    # メインウィンドウの生成
    main_window = MainWindow()
    
    # 各画面の生成
    home_page = HomeWindow()
    drag_drop_page = DragDropWindow()
    
    # メインウィンドウに画面を設定
    main_window.setup_pages(home_page, drag_drop_page)
    
    # 画面切り替え用のシグナル接続
    home_page.switch_to_drag_drop.connect(main_window.switch_to_drag_drop)
    drag_drop_page.switch_to_home.connect(main_window.switch_to_home)
    
    # メインウィンドウを表示
    main_window.show()
    
    sys.exit(app.exec())  # アプリケーションを実行
