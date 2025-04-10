import os
import threading
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QPushButton, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Signal, Qt, Slot
from GUI.utils.file_manager import FileManager
from GUI.components.dropArea import DropArea
from GUI.components.fileListWidget import FileListWidget
from GUI.components.loadingWidget import LoadingWidget
from GUI.components.completionWidget import CompletionWidget
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

        # スタックウィジェットの作成（ドラッグドロップ画面、ローディング画面、完了画面の切り替え用）
        self.stacked_widget = QStackedWidget(self)
        
        # メインのドラッグドロップUI
        self.main_widget = QWidget()
        main_layout = QVBoxLayout(self.main_widget)

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

        # ボタンレイアウト
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addStretch()

        # メインレイアウト設定
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.drop_area)
        main_layout.addWidget(self.file_list_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # ローディングウィジェット
        self.loading_widget = LoadingWidget()
        
        # 完了通知ウィジェット
        self.completion_widget = CompletionWidget()
        self.completion_widget.close_requested.connect(self.on_completion_close)
        
        # スタックウィジェットにページを追加
        self.stacked_widget.addWidget(self.main_widget)
        self.stacked_widget.addWidget(self.loading_widget)
        self.stacked_widget.addWidget(self.completion_widget)
        
        # 全体レイアウト
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # シグナル接続
        self.drop_area.filesDropped.connect(self.file_list_widget.add_files)
        self.file_list_widget.copyRequested.connect(self.on_copy_requested)

    def on_copy_requested(self, files):
        """ コピー実行ボタン押下時の処理 """
        if not files:
            QMessageBox.warning(self, "警告", "コピーするファイルがありません")
            return

        # ファイルをコピー
        copied_files = self.file_manager.copy_files(files)
        if not copied_files:
            QMessageBox.warning(self, "エラー", "ファイルのコピーに失敗しました")
            return
            
        # コピー後にリストをクリア
        self.file_list_widget.clear_files()
        
        # ローディング画面に切り替え
        self.stacked_widget.setCurrentIndex(1)
        
        # バックグラウンドスレッドで処理を実行
        self.process_thread = threading.Thread(target=self.run_processing)
        self.process_thread.daemon = True
        self.process_thread.start()
    
    def run_processing(self):
        """ バックグラウンドでの処理実行 """
        try:
            # main.pyの処理を実行
            import main
            main.main()
            
            # UI操作は必ずメインスレッドから行う
            from PySide6.QtCore import QMetaObject, Qt, Q_ARG
            QMetaObject.invokeMethod(self, "show_completion", Qt.QueuedConnection)
        except Exception as e:
            # エラー発生時の処理
            from PySide6.QtCore import QMetaObject, Qt, Q_ARG
            QMetaObject.invokeMethod(self, "show_error", Qt.QueuedConnection, 
                                    Q_ARG(str, str(e)))
    
    @Slot()
    def show_completion(self):
        """ 処理完了画面を表示する """
        self.stacked_widget.setCurrentIndex(2)
    
    @Slot(str)
    def show_error(self, error_message):
        """ エラーメッセージを表示し、メイン画面に戻る """
        self.stacked_widget.setCurrentIndex(0)
        QMessageBox.critical(self, "エラー", f"処理中にエラーが発生しました:\n{error_message}")
    
    def on_completion_close(self):
        """ 完了画面の閉じるボタンがクリックされた時の処理 """
        self.stacked_widget.setCurrentIndex(0)  # メイン画面に戻る
        
    def on_back_button_clicked(self):
        """戻るボタンがクリックされたらシグナルを発行"""
        self.switch_to_home.emit()
