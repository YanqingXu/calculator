"""计算器主程序"""
import tkinter as tk
from logic import CalculatorLogic
from ui import CalculatorUI
from setting import SettingsManager, SettingsWindow
from history import HistoryManager, HistoryWindow
from keyboard import KeyboardHandler
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE

class Calculator:
    def __init__(self):
        # 创建主窗口
        self.window = tk.Tk()
        self.window.title(WINDOW_TITLE)
        self.window.resizable(False, False)
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        # 初始化各个模块
        self.logic = CalculatorLogic()
        self.history_manager = HistoryManager()
        self.ui = CalculatorUI(self.window, self.handle_button, self.handle_memory, self.toggle_history)
        self.settings_manager = SettingsManager()
        
        # 创建历史记录窗口
        self.history_window = HistoryWindow(
            self.window,
            self.history_manager,
            self.handle_history_select
        )
        
        # 初始化键盘处理器
        self.keyboard_handler = KeyboardHandler(self)
        self.keyboard_handler.bind_keyboard(self.window)
        
        # 应用初始设置
        self.apply_settings(self.settings_manager.settings)
    
    def handle_button(self, button_text):
        """处理按钮点击"""
        if button_text == 'settings':
            self.open_settings()
            return
        
        # 处理内存操作
        if button_text in ['MC', 'MR', 'MS', 'M+', 'M-', 'M▾']:
            if button_text == 'M▾':
                # TODO: 显示内存历史记录
                return
            
            result = self.logic.handle_memory(button_text)
            if result == "错误":
                self.ui.update_display("", "错误", False)
            elif result:  # MR 操作返回内存值
                self.ui.update_display(self.logic.current_expression, result, False)
            # 更新内存指示器
            self.ui.update_memory_indicator(self.logic.has_memory())
            return
        
        result = None
        if button_text.isdigit() or button_text == '.':
            if button_text == '.':
                result = self.logic.handle_decimal()
            else:
                result = self.logic.handle_number(button_text)
            # 更新显示（不显示等号）
            self.ui.update_display(self.logic.current_expression, "", False)
            
        elif button_text in '+-×÷':
            result = self.logic.handle_operator(button_text)
            # 更新显示（不显示等号）
            self.ui.update_display(self.logic.current_expression, "", False)
            
        elif button_text == '=':
            result = self.logic.calculate()
            if result != "错误":
                # 添加到历史记录时包含完整表达式和结果
                history_expression = f"{self.logic.current_expression} = {result}"
                self.history_manager.add_calculation(
                    history_expression,
                    result
                )
            # 更新显示（显示等号和结果）
            self.ui.update_display(self.logic.current_expression, result, True)
            
        elif button_text == 'C':
            result = self.logic.clear_all()
            # 更新显示（清空所有）
            self.ui.update_display("", "0", False)
            
        elif button_text == 'CE':
            result = self.logic.clear_entry()
            # 更新显示（不显示等号）
            self.ui.update_display(self.logic.current_expression, "", False)
            
        elif button_text == '⌫':  # 退格键
            if not self.logic.new_number and self.logic.current_expression:
                self.logic.current_expression = self.logic.current_expression[:-1]
                if not self.logic.current_expression:
                    self.logic.current_expression = "0"
                    self.logic.new_number = True
                # 更新显示（不显示等号）
                self.ui.update_display(self.logic.current_expression, "", False)
                
        elif button_text in ['%', '√', 'x²', '1/x', '±']:
            # TODO: 实现这些功能
            pass
        
    def handle_memory(self, operation):
        """处理内存操作"""
        result = self.logic.handle_memory(operation)
        self.ui.update_display(self.logic.current_expression, result)
    
    def handle_history_select(self, history_item):
        """处理历史记录选择"""
        # 从历史记录中提取表达式和结果
        expression = history_item['expression']
        result = history_item['result']
        
        # 更新计算器状态
        self.logic.current_expression = expression
        self.logic.current_number = result
        self.logic.new_number = True
        
        # 更新显示
        self.ui.update_display(expression, result)
    
    def toggle_history(self):
        """切换历史记录窗口显示状态"""
        self.history_window.show()
    
    def open_settings(self):
        """打开设置窗口"""
        settings_window = SettingsWindow(
            self.window,
            self.settings_manager,
            self.apply_settings
        )
        self.window.wait_window(settings_window.window)
    
    def apply_settings(self, settings):
        """应用设置"""
        # TODO: 实现背景图片设置
        pass
    
    def run(self):
        """运行程序"""
        self.window.mainloop()

if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()
