from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt, Signal
from GUI.styles.stylesheet import DROP_AREA_DEFAULT, DROP_AREA_ACTIVE

class DropArea(QLabel):
    """ドラッグ＆ドロップ機能を持つエリアコンポーネント"""
    
    filesDropped = Signal(list)  # ファイルがドロップされた時に発火するシグナル
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("ここにファイルをドラッグ＆ドロップ")
        self.setAcceptDrops(True)
        self.setMinimumHeight(50)
        self.setStyleSheet(DROP_AREA_DEFAULT)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """ドラッグ時の処理"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet(DROP_AREA_ACTIVE)
    
    def dragLeaveEvent(self, event):
        """ドラッグが外れた時の処理"""
        self.setStyleSheet(DROP_AREA_DEFAULT)
    
    def dropEvent(self, event: QDropEvent):
        """ファイルドロップ時の処理"""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.filesDropped.emit(files)  # シグナル発火
        self.setStyleSheet(DROP_AREA_DEFAULT)