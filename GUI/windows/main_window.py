# windows/main_window.py
import os
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget
from PySide6.QtCore import Qt

from GUI.components.dragdrop_component import DragDropMixin
from GUI.utils.folder_utils import prepare_folder, copy_files

class MainWindow(QWidget, DragDropMixin):
    def __init__(self):
        super().__init__()

        # ウィンドウの設定
        self.setWindowTitle("ドラッグ＆ドロップ - ファイルコピー")
        self.resize(800, 600)  # 好みのサイズに調整

        # ウィジェット生成
        self.label = QLabel("この下にExcelファイルをドラッグ＆ドロップ", self)
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

        # ドラッグ＆ドロップの初期化
        self.init_drag_drop()

        # コピー先フォルダの準備
        self.target_folder = os.path.join(os.getcwd(), "data_folder")
        prepare_folder(self.target_folder)

        # ドラッグ＆ドロップで受け取ったファイルを格納するリスト
        self.file_paths = []

    def copy_files(self):
        """OKボタンが押されたときにファイルをコピー"""
        if not self.file_paths:
            self.label.setText("コピーするファイルがありません")
            return

        copied_files = copy_files(self.file_paths, self.target_folder)
        self.file_list.clear()
        self.file_paths.clear()
        self.label.setText(f"{len(copied_files)} 個のファイルをコピーしました")
