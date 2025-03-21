import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QPushButton, QHBoxLayout
from PySide6.QtCore import Signal, Qt
from GUI.utils.file_manager import FileManager
from GUI.components.dropArea import DropArea
from GUI.components.fileListWidget import FileListWidget
from GUI.styles.stylesheet import MAIN_WINDOW
from dotenv import load_dotenv

load_dotenv()
INPUT_DATA_FOLDER = os.getenv("INPUT_DATA_FILE")

class DragDropWindow(QWidget):
    # 画面遷移用のシグナル
    switch_to_home = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)

        # ファイル管理クラス
        self.file_manager = FileManager(os.path.join(os.getcwd(), INPUT_DATA_FOLDER))
        self.file_manager.reset_folder()

        # コンポーネントの作成
        self.drop_area = DropArea(self)
        self.file_list_widget = FileListWidget(self)
        
        # 戻るボタンの作成
        self.back_button = QPushButton("戻る")
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                border: none;
                border-radius: 5px;
                color: white;
                font-size: 14px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.back_button.clicked.connect(self.on_back_button_clicked)

        # シグナル接続
        self.drop_area.filesDropped.connect(self.file_list_widget.add_files)
        self.file_list_widget.copyRequested.connect(self.copy_files)

        # ボタンレイアウト
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addStretch()

        # メインレイアウト設定
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.drop_area)
        layout.addWidget(self.file_list_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        self.setLayout(layout)

    def copy_files(self, files):
        """ ファイルコピー処理 """
        if not files:
            QMessageBox.warning(self, "警告", "コピーするファイルがありません")
            return

        copied_files = self.file_manager.copy_files(files)

        # コピー後にリストをクリア
        self.file_list_widget.clear_files()
        QMessageBox.information(self, "完了", f"{len(copied_files)} 個のファイルをコピーしました")
        
    def on_back_button_clicked(self):
        """戻るボタンがクリックされたらシグナルを発行"""
        self.switch_to_home.emit()
