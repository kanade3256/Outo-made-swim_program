from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer

class LoadingWidget(QWidget):
    """処理中のローディング表示を行うコンポーネント"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # レイアウト設定
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # 処理中メッセージ
        self.message_label = QLabel("処理中です。しばらくお待ちください...", self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("""
            font-size: 16px;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        
        # プログレスバー
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # 不定のプログレス表示
        self.progress_bar.setFixedSize(300, 20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                width: 10px;
            }
        """)
        
        # レイアウトに追加
        layout.addWidget(self.message_label)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
        self.setFixedSize(400, 200)