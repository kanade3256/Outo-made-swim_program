from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QFileDialog, QLabel

class SaveFileDialogWidget(QWidget):
    """
    保存先ファイルを選択できるウィジェット
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel("保存先ファイルを選択してください：")
        self.path_edit = QLineEdit(self)
        self.path_edit.setReadOnly(True)
        browse_btn = QPushButton("参照")
        browse_btn.clicked.connect(self.open_save_dialog)
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.path_edit)
        h_layout.addWidget(browse_btn)
        layout.addWidget(label)
        layout.addLayout(h_layout)
        self.setLayout(layout)

    def open_save_dialog(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存先を選択", "", "Excel Files (*.xlsx);;All Files (*)")
        if file_path:
            self.path_edit.setText(file_path)

    def get_save_path(self):
        return self.path_edit.text()
