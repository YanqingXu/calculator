"""计算器主程序"""
import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
from modules.calculator_ui import CalculatorUI
from modules.calculator_core import CalculatorCore

class Calculator:
    """计算器应用程序类"""
    def __init__(self):
        self.core = CalculatorCore()
        self.ui = CalculatorUI(self.handle_button, self.handle_memory)
        
        # 恢复背景
        if self.ui.background_manager.current_background:
            # 获取窗口大小
            width = self.ui.width()
            height = self.ui.height()
            bg_image = self.ui.background_manager.get_background(width, height)
            if bg_image:
                self.ui.update_background(bg_image)
    
    def format_expression(self, num):
        """格式化表达式中的数字"""
        try:
            float_num = float(num)
            if float_num.is_integer():
                return str(int(float_num))
            return str(float_num)
        except:
            return str(num)
    
    def handle_button(self, text):
        """处理按钮点击"""
        expression = ""
        result = ""
        
        if text.isdigit():
            self.core.number_press(text)
            # 如果有运算符，显示完整算式
            if self.core.previous_num is not None and self.core.operation:
                expression = f"{self.format_expression(self.core.previous_num)} {self.core.operation} {self.core.current_num}"
            else:
                expression = self.core.current_num
        elif text == '.':
            self.core.decimal_press()
            if self.core.previous_num is not None and self.core.operation:
                expression = f"{self.format_expression(self.core.previous_num)} {self.core.operation} {self.core.current_num}"
            else:
                expression = self.core.current_num
        elif text in ['+', '-', '×', '÷']:
            self.core.operation_press(text)
            expression = f"{self.format_expression(self.core.previous_num)} {text}"
        elif text == '=' or text in [Qt.Key_Return, Qt.Key_Enter]:
            if self.core.previous_num is not None and self.core.operation:
                expression = f"{self.format_expression(self.core.previous_num)} {self.core.operation} {self.core.current_num} ="
                result = self.core.calculate()
        elif text == '⌫':
            self.core.backspace()
            if self.core.previous_num is not None and self.core.operation:
                expression = f"{self.format_expression(self.core.previous_num)} {self.core.operation} {self.core.current_num}"
            else:
                expression = self.core.current_num
        elif text == 'C':
            self.core.clear_all()
        elif text == 'CE':
            self.core.clear_entry()
            if self.core.previous_num is not None and self.core.operation:
                expression = f"{self.format_expression(self.core.previous_num)} {self.core.operation}"
        else:
            # 特殊运算
            current = self.core.current_num
            if text == '%':
                expression = f"{current}%"
            elif text == '±':
                expression = f"-({current})"
            elif text == 'x²':
                expression = f"pow({current})"
            elif text == '√':
                expression = f"√({current})"
            elif text == '1/x':
                expression = f"1/({current})"
            
            # 立即计算结果
            result = self.core.special_operation(text)
            # 更新表达式以显示结果
            if result != "错误" and result != "无效输入" and result != "除数不能为零":
                if text == '%':
                    expression = f"{current}% = {result}"
                elif text == '±':
                    expression = f"-({current}) = {result}"
                elif text == 'x²':
                    expression = f"pow({current}) = {result}"
                elif text == '√':
                    expression = f"√({current}) = {result}"
                elif text == '1/x':
                    expression = f"1/({current}) = {result}"
        
        self.ui.update_display(expression, result)
    
    def handle_memory(self, operation):
        """处理内存操作"""
        self.core.memory_operation(operation.upper())
        self.ui.update_memory_indicator(self.core.has_memory)
    
    def run(self):
        """运行应用程序"""
        self.ui.show()

def main():
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.run()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
