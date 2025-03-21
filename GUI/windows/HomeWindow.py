import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal
from GUI.styles.stylesheet import MAIN_WINDOW
from dotenv import load_dotenv

# 環境変数から設定を読み込む
load_dotenv()
APP_NAME = os.getenv("APP_NAME", "AquaProgrammer")  # デフォルト値として"AquaProgrammer"を設定

class HomeWindow(QWidget):
    # 画面遷移用のシグナル
    switch_to_drag_drop = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)

        # レイアウト設定
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 40, 30, 40)
        layout.setSpacing(20)

        # タイトルラベル
        title_label = QLabel(APP_NAME)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 30px;
        """)
        
        # サブタイトルラベル
        subtitle_label = QLabel("水泳競技プログラム自動作成支援ツール")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            font-size: 18px;
            color: #34495e;
            margin-bottom: 40px;
        """)

        # ボタン作成
        start_button = QPushButton("プログラム製作を開始する")
        start_button.setCursor(Qt.PointingHandCursor)
        start_button.setMinimumHeight(50)
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                border: none;
                border-radius: 5px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
        """)
        
        # ボタンクリック時のイベント接続
        start_button.clicked.connect(self.on_start_button_clicked)
        
        # レイアウトにウィジェットを追加
        layout.addStretch(1)  # 上部に余白を作る
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addStretch(1)  # 中央に余白を作る
        layout.addWidget(start_button)
        layout.addStretch(2)  # 下部に余白を作る
        
        self.setLayout(layout)

    def on_start_button_clicked(self):
        """スタートボタンがクリックされたらシグナルを発行"""
        self.switch_to_drag_drop.emit()