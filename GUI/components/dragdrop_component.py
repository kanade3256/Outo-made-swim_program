# components/dragdrop_component.py
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt

class DragDropMixin:
    """ドラッグ＆ドロップ機能を提供するMixin"""

    def init_drag_drop(self):
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """ファイルがドラッグされたときの処理"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """ファイルがドロップされたときの処理"""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        for file in files:
            if file not in getattr(self, 'file_paths', []):
                self.file_paths.append(file)
                self.file_list.addItem(file)
