"""键盘事件处理模块"""
from PySide2.QtCore import Qt

class KeyboardHandler:
    """键盘事件处理器"""
    def __init__(self, callback):
        self.callback = callback
    
    def handle_key_press(self, event):
        """处理键盘事件"""
        key = event.key()
        text = event.text()
        
        # 数字键（包括主键盘和小键盘）
        if text.isdigit():
            self.callback(text)
        # 运算符
        elif key == Qt.Key_Plus:
            self.callback('+')
        elif key == Qt.Key_Minus:
            self.callback('-')
        elif key == Qt.Key_Asterisk:
            self.callback('×')
        elif key == Qt.Key_Slash:
            self.callback('÷')
        # 回车和等号键
        elif key in [Qt.Key_Return, Qt.Key_Enter, Qt.Key_Equal]:
            self.callback('=')
        # 退格键
        elif key == Qt.Key_Backspace:
            self.callback('⌫')
        # 删除键
        elif key == Qt.Key_Delete:
            self.callback('C')
        # Escape键
        elif key == Qt.Key_Escape:
            self.callback('CE')
        # 小数点
        elif key == Qt.Key_Period:
            self.callback('.')
        # 百分号
        elif key == Qt.Key_Percent:
            self.callback('%')
