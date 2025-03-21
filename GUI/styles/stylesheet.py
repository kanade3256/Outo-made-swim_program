"""
アプリケーション全体で使用するスタイルシートを定義するモジュール
"""

# ドロップエリア用スタイル
DROP_AREA_DEFAULT = """
    border: 2px dashed #aaaaaa;
    border-radius: 5px;
    padding: 15px;
    font-size: 14px;
"""

DROP_AREA_ACTIVE = """
    border: 2px solid #3498db;
    border-radius: 5px;
    background-color: #e8f4fc;
    padding: 15px;
    font-size: 14px;
"""

# ファイルリストウィジェット用スタイル
FILE_LIST_WIDGET = """
    QListWidget {
        border: 1px solid #cccccc;
        border-radius: 3px;
        padding: 5px;
    }
    
    QListWidget::item {
        padding: 5px;
        border-bottom: 1px solid #eeeeee;
    }
    
    QListWidget::item:selected {
        background-color: #e8f4fc;
        color: #333333;
    }
"""

# ボタン用スタイル
BUTTON_DEFAULT = """
    QPushButton {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 3px;
        padding: 8px 16px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #2980b9;
    }
    
    QPushButton:pressed {
        background-color: #1a5276;
    }
"""

# メインウィンドウ用スタイル
MAIN_WINDOW = """
    QWidget {
        background-color: #f9f9f9;
    }
"""

def get_application_style():
    """アプリケーション全体のスタイルシートを返します"""
    return MAIN_WINDOW