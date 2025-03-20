import os
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget, QMessageBox
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt
from GUI.utils.file_manager import FileManager  # ファイル管理クラスをインポート
from dotenv import load_dotenv

load_dotenv()
INPUT_DATA_FOLDER = os.getenv("INPUT_DATA_FILE")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.setWindowTitle("ドラッグ＆ドロップ - ファイルコピー")
        self.setGeometry(100, 100, 400, 400)

        # ファイル管理クラス
        self.file_manager = FileManager(os.path.join(os.getcwd(), INPUT_DATA_FOLDER))
        self.file_manager.reset_folder()

        # UI要素
        self.label = QLabel("ここにファイルをドラッグ＆ドロップ", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_list = QListWidget(self)
        self.ok_button = QPushButton("OK (コピー実行)", self)
        self.ok_button.clicked.connect(self.copy_files)

        # レイアウト設定
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.file_list)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

        # ドラッグ＆ドロップ有効化
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """ ドラッグ時の処理 """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """ ファイルドロップ時の処理 """
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        existing_files = {self.file_list.item(i).text() for i in range(self.file_list.count())}

        for file in files:
            if file not in existing_files:
                self.file_list.addItem(file)

    def copy_files(self):
        """ OKボタン押下時のファイルコピー処理 """
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "警告", "コピーするファイルがありません")
            return

        files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        copied_files = self.file_manager.copy_files(files)

        # コピー後にリストをクリア
        self.file_list.clear()
        QMessageBox.information(self, "完了", f"{len(copied_files)} 個のファイルをコピーしました")
