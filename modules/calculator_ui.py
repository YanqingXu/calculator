"""计算器UI模块"""
from PySide2.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QFrame, QGridLayout)
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont, QImage, QPixmap
from .base_widget import BackgroundWidget
from .background_manager import BackgroundManager
from .keyboard_handler import KeyboardHandler
from .history_manager import HistoryManager

class CalculatorUI(QMainWindow):
    """计算器UI类"""
    def __init__(self, button_callback, memory_callback):
        super().__init__()
        self.button_callback = button_callback
        self.memory_callback = memory_callback
        self.background_manager = BackgroundManager()
        self.keyboard_handler = KeyboardHandler(self.button_callback)
        self.history_manager = HistoryManager()
        
        # 设置窗口属性
        self.setWindowTitle("计算器")
        self.setMinimumSize(400, 600)
        
        # 创建背景部件
        self.background_widget = BackgroundWidget(self)
        self.setCentralWidget(self.background_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(self.background_widget)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 设置样式
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 180);
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(240, 240, 240, 180);
            }
            QPushButton:pressed {
                background-color: rgba(220, 220, 220, 180);
            }
            QLabel {
                background-color: rgba(255, 255, 255, 180);
                padding: 5px;
            }
            QFrame {
                background-color: rgba(255, 255, 255, 180);
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)
        
        # 创建标题栏
        title_bar = QHBoxLayout()
        
        # 添加设置按钮（左侧）
        settings_button = QPushButton("⚙")
        settings_button.setFixedSize(40, 40)
        settings_button.clicked.connect(lambda: self.background_manager.show_settings(self))
        title_bar.addWidget(settings_button)
        
        title_bar.addStretch()  # 添加弹性空间
        
        # 添加历史记录按钮（右侧）
        history_button = QPushButton("📋")
        history_button.setFixedSize(40, 40)
        history_button.clicked.connect(lambda: self.history_manager.show_history(self))
        title_bar.addWidget(history_button)
        
        main_layout.addLayout(title_bar)
        
        # 创建显示区域
        display_frame = QFrame()
        display_frame.setFrameStyle(QFrame.Box)
        display_layout = QVBoxLayout(display_frame)
        display_layout.setSpacing(5)
        
        # 算式显示
        self.expression_label = QLabel("")
        self.expression_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.expression_label.setFont(QFont("Arial", 14))
        self.expression_label.setStyleSheet("color: #666;")
        self.expression_label.setMinimumHeight(30)
        
        # 结果显示
        self.result_label = QLabel("0")
        self.result_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.result_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.result_label.setMinimumHeight(50)
        
        display_layout.addWidget(self.expression_label)
        display_layout.addWidget(self.result_label)
        main_layout.addWidget(display_frame)
        
        # 创建内存按钮区域
        memory_layout = QHBoxLayout()
        memory_buttons = [
            ('MC', 'memory_clear'),
            ('MR', 'memory_recall'),
            ('M+', 'memory_add'),
            ('M-', 'memory_subtract'),
            ('MS', 'memory_store')
        ]
        
        for text, command in memory_buttons:
            btn = QPushButton(text)
            btn.setFont(QFont("Arial", 10))
            btn.clicked.connect(self.create_memory_callback(command))
            memory_layout.addWidget(btn)
        
        # 添加内存指示器
        self.memory_indicator = QLabel("M")
        self.memory_indicator.setFont(QFont("Arial", 10))
        self.memory_indicator.hide()
        memory_layout.addWidget(self.memory_indicator)
        
        main_layout.addLayout(memory_layout)
        
        # 添加分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # 创建按钮网格
        button_grid = QGridLayout()
        button_grid.setSpacing(5)
        
        button_texts = [
            ['%', 'CE', 'C', '⌫'],
            ['1/x', 'x²', '√', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]
        
        for i, row_texts in enumerate(button_texts):
            for j, text in enumerate(row_texts):
                btn = QPushButton(text)
                btn.setFont(QFont("Arial", 12))
                btn.clicked.connect(self.create_button_callback(text))
                button_grid.addWidget(btn, i, j)
        
        main_layout.addLayout(button_grid)
        
        # 设置背景管理器的回调
        self.background_manager.set_callback(self.update_background)
    
    def create_button_callback(self, text):
        """创建按钮回调函数"""
        def callback():
            self.button_callback(text)
        return callback
    
    def create_memory_callback(self, command):
        """创建内存按钮回调函数"""
        def callback():
            self.memory_callback(command)
        return callback
    
    def update_display(self, expression, result):
        """更新显示内容"""
        self.expression_label.setText(expression)
        self.result_label.setText(result)
        # 添加到历史记录
        if expression and result and ('=' in expression or expression.startswith(('pow', '√', '1/'))):
            self.history_manager.add_record(expression, result)
    
    def update_memory_indicator(self, has_memory):
        """更新内存指示器显示状态"""
        if has_memory:
            self.memory_indicator.show()
        else:
            self.memory_indicator.hide()
    
    def update_background(self, background_image=None):
        """更新背景图片"""
        if background_image:
            # 从PIL Image转换为QImage
            img_data = background_image.tobytes('raw', 'RGBA')
            qimage = QImage(img_data, background_image.width, background_image.height, QImage.Format.Format_RGBA8888)
            
            # 转换为QPixmap并设置给背景部件
            pixmap = QPixmap.fromImage(qimage)
            self.background_widget.setBackgroundPixmap(pixmap)
        else:
            self.background_widget.setBackgroundPixmap(None)
    
    def resizeEvent(self, event):
        """窗口大小改变时更新背景"""
        super().resizeEvent(event)
        if hasattr(self.background_manager, 'current_background'):
            size = event.size()
            bg_image = self.background_manager.get_background(size.width(), size.height())
            if bg_image:
                self.update_background(bg_image)
    
    def keyPressEvent(self, event):
        """处理键盘事件"""
        self.keyboard_handler.handle_key_press(event)
