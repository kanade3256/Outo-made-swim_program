from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QFileDialog, QLabel

class SelectFolderDialogWidget(QWidget):
    """
    保存先フォルダーを選択できるウィジェット
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel("保存先フォルダーを選択してください：")
        self.path_edit = QLineEdit(self)
        self.path_edit.setReadOnly(True)
        browse_btn = QPushButton("参照")
        browse_btn.clicked.connect(self.open_folder_dialog)
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.path_edit)
        h_layout.addWidget(browse_btn)
        layout.addWidget(label)
        layout.addLayout(h_layout)
        self.setLayout(layout)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "保存先フォルダーを選択")
        if folder_path:
            self.path_edit.setText(folder_path)

    def get_folder_path(self):
        return self.path_edit.text()
