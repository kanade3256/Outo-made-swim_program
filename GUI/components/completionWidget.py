from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal

class CompletionWidget(QWidget):
    """処理完了通知を表示するコンポーネント"""
    
    close_requested = Signal()  # 閉じるボタンが押された時に発火するシグナル
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # レイアウト設定
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # 完了メッセージ
        self.message_label = QLabel("プログラムの作成が完了しました", self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("""
            font-size: 18px;
            color: #2c3e50;
            margin-bottom: 30px;
            font-weight: bold;
        """)
        
        # 閉じるボタン
        self.close_button = QPushButton("閉じる", self)
        self.close_button.setFixedSize(120, 40)
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                border: none;
                border-radius: 5px;
                color: white;
                font-size: 14px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.close_button.clicked.connect(self._on_close_clicked)
        
        # レイアウトに追加
        layout.addWidget(self.message_label)
        layout.addWidget(self.close_button)
        
        self.setLayout(layout)
        self.setFixedSize(400, 200)
    
    def _on_close_clicked(self):
        """閉じるボタンがクリックされた時の処理"""
        self.close_requested.emit()