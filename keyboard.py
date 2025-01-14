"""键盘输入处理模块"""

class KeyboardHandler:
    def __init__(self, calculator):
        self.calculator = calculator
        
        # 键盘映射
        self.key_mappings = {
            # 数字键和小数点
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '.': '.',
            
            # 数字键盘
            'KP_0': '0', 'KP_1': '1', 'KP_2': '2', 'KP_3': '3', 'KP_4': '4',
            'KP_5': '5', 'KP_6': '6', 'KP_7': '7', 'KP_8': '8', 'KP_9': '9',
            'KP_Decimal': '.',
            
            # 运算符
            'plus': '+', 'minus': '-', 'asterisk': '×', 'slash': '÷',
            'KP_Add': '+', 'KP_Subtract': '-', 'KP_Multiply': '×', 'KP_Divide': '÷',
            
            # 功能键
            'Return': '=', 'KP_Enter': '=',
            'BackSpace': '⌫',
            'Delete': 'CE',
            'Escape': 'C',
            
            # 特殊功能
            'percent': '%',
            'asciicircum': 'x²',  # ^ 键
            'r': '√',  # r 键
            'v': '1/x',  # v 键
        }
    
    def handle_keypress(self, event):
        """处理键盘按键事件"""
        # 获取按键名称
        key_name = event.keysym
        
        # 检查是否是已映射的按键
        if key_name in self.key_mappings:
            button_text = self.key_mappings[key_name]
            self.calculator.handle_button(button_text)
            return "break"  # 阻止事件继续传播
        
        return None  # 允许其他按键正常工作
    
    def bind_keyboard(self, window):
        """绑定键盘事件到窗口"""
        window.bind('<Key>', self.handle_keypress)
        # 为数字键盘的加号单独绑定，因为它可能与shift+等号冲突
        window.bind('<KP_Add>', lambda e: self.handle_keypress(e))
