"""计算器UI模块"""
from PySide2.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QFrame, QGridLayout,
                           QMenu, QApplication, QLineEdit)
from PySide2.QtCore import Qt, QTimer, QObject, QEvent
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
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                padding: 5px;
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
        self.expression_display = QLabel("")  # 显示控件
        self.expression_display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.expression_display.setFont(QFont("Arial", 14))
        self.expression_display.setStyleSheet("color: #666;")
        self.expression_display.setMinimumHeight(30)
        self.expression_display.setContextMenuPolicy(Qt.CustomContextMenu)
        self.expression_display.customContextMenuRequested.connect(self.show_context_menu)
        self.expression_display.mousePressEvent = self.switch_to_input_mode

        # 算式输入
        self.expression_input = QLineEdit()  # 输入控件
        self.expression_input.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.expression_input.setFont(QFont("Arial", 14))
        self.expression_input.setStyleSheet("color: #666;")
        self.expression_input.setMinimumHeight(30)
        self.expression_input.hide()  # 初始隐藏输入控件
        self.expression_input.editingFinished.connect(self.finish_input)
        self.expression_input.installEventFilter(self)  # 安装事件过滤器
        
        # 结果显示
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.result_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.result_label.setMinimumHeight(50)
        self.result_label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.result_label.customContextMenuRequested.connect(self.show_context_menu)
        
        display_layout.addWidget(self.expression_display)
        display_layout.addWidget(self.expression_input)
        display_layout.addWidget(self.result_label)
        main_layout.addWidget(display_frame)
        
        # 初始化键盘处理器（确保在创建完expression_display后初始化）
        self.keyboard_handler = KeyboardHandler(self.button_callback, self.expression_display)
        
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
        
        # 安装事件过滤器
        self.installEventFilter(self)

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
        self.expression_display.setText(expression)
        if result:  # 只有在有结果时才更新结果显示
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
    
    def show_context_menu(self, position):
        """显示右键菜单"""
        sender = self.sender()
        menu = QMenu()
        
        # 添加复制操作
        copy_action = menu.addAction("复制")
        copy_action.triggered.connect(lambda: self.copy_text(sender))
        copy_action.setShortcut("Ctrl+C")
        
        # 添加粘贴操作（仅当剪贴板中有文本时启用）
        clipboard = QApplication.clipboard()
        paste_action = menu.addAction("粘贴")
        paste_action.triggered.connect(self.paste_text)
        paste_action.setShortcut("Ctrl+V")
        paste_action.setEnabled(bool(clipboard.text()))
        
        menu.exec_(sender.mapToGlobal(position))
    
    def copy_text(self, label):
        """复制文本到剪贴板"""
        text = label.text()
        if text:
            QApplication.clipboard().setText(text)
    
    def paste_text(self):
        """从剪贴板粘贴文本"""
        text = QApplication.clipboard().text()
        if text:
            # 尝试将粘贴的文本作为按钮输入处理
            for char in text:
                if char.isdigit() or char in ['+', '-', '×', '÷', '.', '=']:
                    self.button_callback(char)
    
    def keyPressEvent(self, event):
        """处理主窗口的按键事件"""
        # 在显示模式下处理按键输入
        if not self.expression_input.isVisible():
            # 如果keyboard_handler没有处理按键，则尝试处理复制粘贴
            if not self.keyboard_handler.handle_key_press(event):
                if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
                    if self.result_label.text():
                        self.copy_text(self.result_label)
                    else:
                        self.copy_text(self.expression_display)
                elif event.key() == Qt.Key_V and event.modifiers() == Qt.ControlModifier:
                    self.paste_from_clipboard()
        
        # 在输入模式下，Enter键结束输入并计算
        elif event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            self.finish_input(calculate=True)
        
        super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        """事件过滤器，处理输入控件的焦点丢失事件和按键事件"""
        if obj == self.expression_input:
            if event.type() == QEvent.FocusOut:
                self.finish_input(calculate=False)  # 失去焦点时不计算
            elif event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key_Escape:
                    # ESC键取消输入
                    self.cancel_input()
                    return True
                elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                    # Enter键结束输入并计算
                    self.finish_input(calculate=True)
                    return True
        elif event.type() == QEvent.MouseButtonPress:
            # 如果输入控件可见，且点击的不是输入控件
            if self.expression_input.isVisible() and obj != self.expression_input:
                # 结束输入状态
                self.finish_input(calculate=True)
                return True
        return super().eventFilter(obj, event)

    def finish_input(self, calculate=False):
        """完成输入"""
        if self.expression_input.isVisible():
            text = self.expression_input.text()
            if text:  # 只有在有输入内容时才更新显示
                self.expression_input.hide()
                self.expression_display.show()
                if calculate:
                    # 先发送表达式进行计算
                    self.button_callback(text + "=")
                    # 然后更新显示
                    self.expression_display.setText(text)
                else:
                    self.expression_display.setText(text)

    def switch_to_input_mode(self, event=None):
        """切换到输入模式"""
        if event and event.button() != Qt.LeftButton:
            return
        
        # 获取当前表达式和结果
        text = self.expression_display.text()
        result = self.result_label.text()
        
        # 如果有结果且表达式以等号结尾，使用结果作为新表达式的开始
        if result and text.endswith('='):
            text = result
        elif text.endswith('='):
            text = text[:-1].strip()  # 移除等号并清除末尾空格
        
        self.expression_input.setText(text)
        self.expression_display.hide()
        self.expression_input.show()
        self.expression_input.setFocus()
        self.expression_input.setCursorPosition(len(self.expression_input.text()))

    def cancel_input(self):
        """取消输入"""
        if self.expression_input.isVisible():
            self.expression_input.hide()
            self.expression_display.show()

    def switch_to_display_mode(self):
        """切换到显示模式 - 已废弃，使用 finish_input 代替"""
        pass

    def handle_mouse_click(self, event):
        """移除旧的鼠标点击处理方法"""
        pass

    def get_text_without_cursor(self):
        """移除旧的光标处理方法"""
        pass

    def update_display_with_cursor(self):
        """移除旧的光标更新方法"""
        pass

    def blink_cursor(self):
        """移除旧的光标闪烁方法"""
        pass

    def clear_all_display(self):
        """清除所有显示内容"""
        self.expression_display.clear()
        self.expression_input.clear()
        self.result_label.clear()

    def clear_result(self):
        """清除结果显示"""
        self.result_label.clear()

    def resizeEvent(self, event):
        """窗口大小改变时更新背景"""
        super().resizeEvent(event)
        if hasattr(self.background_manager, 'current_background'):
            size = event.size()
            bg_image = self.background_manager.get_background(size.width(), size.height())
            if bg_image:
                self.update_background(bg_image)
