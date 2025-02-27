import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget
from PySide6.QtCore import Qt
from GUI.utils.dragdrop import DragDropMixin
from GUI.utils.file_handler import FileHandler

class MainWindow(QWidget, DragDropMixin):
    def __init__(self):
        super().__init__()

        # ウィンドウの設定
        self.setWindowTitle("ドラッグ＆ドロップ - ファイルコピー")
        self.resize(600, 400)

        # 説明用ラベル
        self.label = QLabel("この下にExcelファイルをドラッグ＆ドロップ", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ドロップされたファイルの一覧表示用ウィジェット
        self.file_list = QListWidget(self)

        # OKボタン（コピーを実行）
        self.ok_button = QPushButton("OK (コピー実行)", self)
        self.ok_button.clicked.connect(self.copy_files)

        # レイアウト設定
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.file_list)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

        # ドラッグ＆ドロップの設定
        self.init_drag_drop()

        # ファイル管理インスタンス
        self.file_handler = FileHandler()

    def copy_files(self):
        """ OKボタンが押されたときにファイルをコピー """
        if not self.file_paths:
            self.label.setText("コピーするファイルがありません")
            return

        copied_files = self.file_handler.copy_files(self.file_paths)
        self.file_list.clear()
        self.file_paths.clear()
        self.label.setText(f"{len(copied_files)} 個のファイルを 'data/folder' にコピーしました")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
