"""键盘事件处理模块"""
from PySide2.QtCore import Qt

class KeyboardHandler:
    """键盘事件处理器"""
    def __init__(self, button_callback, expression_display):
        self.button_callback = button_callback
        self.expression_display = expression_display
    
    def handle_key_press(self, event):
        """处理键盘事件"""
        key = event.key()
        text = event.text()
        
        # 处理Ctrl+C（复制）
        if key == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
            return False  # 让主窗口处理复制操作
            
        # 处理Ctrl+V（粘贴）
        elif key == Qt.Key_V and event.modifiers() == Qt.ControlModifier:
            return False  # 让主窗口处理粘贴操作
        
        # 数字键（包括主键盘和小键盘）
        elif text.isdigit():
            self.button_callback(text)
            return True
            
        # 运算符
        elif key == Qt.Key_Plus:
            self.button_callback('+')
            return True
        elif key == Qt.Key_Minus:
            self.button_callback('-')
            return True
        elif key == Qt.Key_Asterisk:
            self.button_callback('×')
            return True
        elif key == Qt.Key_Slash:
            self.button_callback('÷')
            return True
            
        # Enter键和等号键都触发计算
        elif key in [Qt.Key_Return, Qt.Key_Enter, Qt.Key_Equal]:
            # 如果有表达式，添加等号并计算
            expression = self.expression_display.text()
            if expression and not expression.endswith('='):
                self.button_callback(expression + "=")
            return True
            
        # 退格键
        elif key == Qt.Key_Backspace:
            self.button_callback('⌫')
            return True
            
        # 删除键
        elif key == Qt.Key_Delete:
            self.button_callback('C')
            return True
            
        # Escape键
        elif key == Qt.Key_Escape:
            self.button_callback('CE')
            return True
            
        # 小数点
        elif key == Qt.Key_Period:
            self.button_callback('.')
            return True
            
        # 百分号
        elif key == Qt.Key_Percent:
            self.button_callback('%')
            return True
            
        return False  # 未处理的按键
