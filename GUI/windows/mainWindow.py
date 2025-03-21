import os
from PySide6.QtWidgets import QMainWindow, QStackedWidget
from PySide6.QtCore import Qt
from GUI.styles.stylesheet import MAIN_WINDOW
from dotenv import load_dotenv

# 環境変数から設定を読み込む
load_dotenv()
APP_NAME = os.getenv("APP_NAME", "AquaProgrammer")  # デフォルト値として"AquaProgrammer"を設定

class MainWindow(QMainWindow):
    """
    アプリケーションのメインウィンドウ。
    QStackedWidgetを使用して異なる画面間をシームレスに切り替えます。
    """
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet(MAIN_WINDOW)

        # スタックウィジェットのセットアップ
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 画面インスタンスはMainWindow生成後に作成される
        self.home_page = None
        self.drag_drop_page = None
        
    def setup_pages(self, home_page, drag_drop_page):
        """異なる画面をスタックに追加する"""
        self.home_page = home_page
        self.drag_drop_page = drag_drop_page
        
        # スタックにページを追加
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.drag_drop_page)
        
        # 最初はホーム画面を表示
        self.stacked_widget.setCurrentIndex(0)
        
    def switch_to_home(self):
        """ホーム画面に切り替え"""
        self.stacked_widget.setCurrentIndex(0)
        
    def switch_to_drag_drop(self):
        """ドラッグ&ドロップ画面に切り替え"""
        self.stacked_widget.setCurrentIndex(1)