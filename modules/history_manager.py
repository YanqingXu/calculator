"""历史记录管理器模块"""
from PySide2.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QLabel
from PySide2.QtCore import Qt

class HistoryManager:
    """历史记录管理器类"""
    def __init__(self):
        self.history = []
        self.dialog = None
    
    def add_record(self, expression, result):
        """添加一条历史记录"""
        if expression and result:
            record = f"{expression} {result}"
            self.history.append(record)
            # 最多保存100条记录
            if len(self.history) > 100:
                self.history.pop(0)
    
    def show_history(self, parent=None):
        """显示历史记录对话框"""
        if not self.dialog:
            self.dialog = QDialog(parent)
            self.dialog.setWindowTitle("计算历史")
            self.dialog.setMinimumSize(300, 400)
            
            # 设置样式
            self.dialog.setStyleSheet("""
                QDialog {
                    background-color: rgba(255, 255, 255, 240);
                }
                QListWidget {
                    background-color: rgba(255, 255, 255, 180);
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 5px;
                }
                QPushButton {
                    background-color: rgba(255, 255, 255, 180);
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: rgba(240, 240, 240, 180);
                }
                QLabel {
                    color: #666;
                    padding: 5px;
                }
            """)
            
            # 创建布局
            layout = QVBoxLayout(self.dialog)
            
            # 添加标题
            title = QLabel("计算历史记录")
            title.setAlignment(Qt.AlignCenter)
            layout.addWidget(title)
            
            # 创建列表控件
            self.list_widget = QListWidget()
            layout.addWidget(self.list_widget)
            
            # 添加清除按钮
            clear_button = QPushButton("清除历史记录")
            clear_button.clicked.connect(self.clear_history)
            layout.addWidget(clear_button)
            
            # 添加关闭按钮
            close_button = QPushButton("关闭")
            close_button.clicked.connect(self.dialog.close)
            layout.addWidget(close_button)
        
        # 更新列表内容
        self.list_widget.clear()
        for record in reversed(self.history):  # 最新的记录显示在顶部
            self.list_widget.addItem(record)
        
        self.dialog.show()
    
    def clear_history(self):
        """清除历史记录"""
        self.history.clear()
        if self.dialog:
            self.list_widget.clear()
