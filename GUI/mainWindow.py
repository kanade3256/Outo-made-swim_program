import sys
import os
import shutil
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # ウィンドウの設定
        self.setWindowTitle("ドラッグ＆ドロップ - ファイルコピー")
        self.setGeometry(100, 100, 400, 400)

        # 説明用ラベル
        self.label = QLabel("ここにファイルをドラッグ＆ドロップ", self)
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

        # ドラッグ＆ドロップの有効化
        self.setAcceptDrops(True)

        # "folder" フォルダのパス設定
        self.target_folder = os.path.join(os.getcwd(), "folder")

        # プログラム起動時に "folder" の中身をリセット（存在する場合は削除）
        if os.path.exists(self.target_folder):
            for filename in os.listdir(self.target_folder):
                file_path = os.path.join(self.target_folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
        else:
            os.makedirs(self.target_folder, exist_ok=True)

        # ドラッグ＆ドロップで受け取ったファイルパスを格納するリスト
        self.file_paths = []

    def dragEnterEvent(self, event: QDragEnterEvent):
        """ ファイルがドラッグされたときの処理 """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """ ファイルがドロップされたときの処理（コピーはまだ実行しない） """
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        for file in files:
            if file not in self.file_paths:  # 重複追加を防止
                self.file_paths.append(file)
                self.file_list.addItem(file)

    def copy_files(self):
        """ OKボタンが押されたときにファイルをコピー """
        if not self.file_paths:
            self.label.setText("コピーするファイルがありません")
            return

        copied_files = []
        for file_path in self.file_paths:
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(self.target_folder, file_name)
            shutil.copy2(file_path, dest_path)  # 移動ではなくコピー
            copied_files.append(dest_path)

        # コピー後、リストとファイルパスのリストをリセット
        self.file_list.clear()
        self.file_paths.clear()
        self.label.setText(f"{len(copied_files)} 個のファイルを 'folder' にコピーしました")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DragDropWindow()
    window.show()