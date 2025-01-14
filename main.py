"""计算器主程序"""
import tkinter as tk
from tkinter import ttk
from logic import CalculatorLogic
from ui import CalculatorUI
from setting import SettingsManager, SettingsWindow
from history import HistoryManager, HistoryWindow
from keyboard import KeyboardHandler
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from background import BackgroundManager

class Calculator:
    def __init__(self):
        # 创建主窗口
        self.window = tk.Tk()
        self.window.title(WINDOW_TITLE)
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.window.resizable(False, False)
        
        # 初始化各个模块
        self.logic = CalculatorLogic()
        self.history_manager = HistoryManager()
        self.background_manager = BackgroundManager()
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
        
        # 防止频繁更新的标志
        self.resize_after_id = None
        
        # 绑定窗口大小变化事件
        self.window.bind('<Configure>', self.on_window_resize)
        
        # 等待窗口完全显示后再加载背景
        self.window.update_idletasks()
        self.window.after(100, self.update_background)  # 延迟100ms加载背景
    
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
        dialog = tk.Toplevel(self.window)
        dialog.title("背景设置")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.transient(self.window)  # 设置为主窗口的临时窗口
        
        # 设置按钮样式
        style = ttk.Style()
        style.configure('Settings.TButton',
                       padding=10,
                       width=20)
        
        # 设置按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(expand=True)
        
        # 选择背景按钮
        select_btn = ttk.Button(
            button_frame,
            text="选择背景图片",
            style='Settings.TButton',
            command=lambda: self.select_background(dialog)
        )
        select_btn.pack(pady=10)
        
        # 清除背景按钮
        clear_btn = ttk.Button(
            button_frame,
            text="清除背景",
            style='Settings.TButton',
            command=lambda: self.clear_background(dialog)
        )
        clear_btn.pack(pady=10)
        
        # 关闭按钮
        close_btn = ttk.Button(
            button_frame,
            text="关闭",
            style='Settings.TButton',
            command=dialog.destroy
        )
        close_btn.pack(pady=10)
        
        # 设置为模态窗口
        dialog.grab_set()
        dialog.focus_set()
        
        # 将窗口居中显示
        dialog.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() - dialog.winfo_width()) // 2
        y = self.window.winfo_y() + (self.window.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
    
    def select_background(self, dialog):
        """选择背景图片"""
        try:
            if self.background_manager.select_background():
                self.update_background()
                dialog.destroy()
        except Exception as e:
            print(f"选择背景图片时出错: {e}")
    
    def clear_background(self, dialog):
        """清除背景"""
        try:
            self.background_manager.clear_background()
            self.update_background()
            dialog.destroy()
        except Exception as e:
            print(f"清除背景时出错: {e}")
    
    def update_background(self):
        """更新背景图片"""
        # 重置延迟更新标志
        self.resize_after_id = None
        
        try:
            if self.background_manager.current_background:
                print("正在更新背景...")
                # 获取实际窗口大小
                width = self.window.winfo_width()
                height = self.window.winfo_height()
                print(f"当前窗口大小: {width}x{height}")
                
                if width > 0 and height > 0:  # 确保窗口大小有效
                    background = self.background_manager.get_background(width, height)
                    if background:  # 确保成功获取到背景图片
                        print("成功获取背景图片")
                        self.ui.update_background(background)
                    else:
                        print("获取背景图片失败")
                else:
                    print("窗口大小无效")
            else:
                print("无背景图片")
                self.ui.update_background(None)
        except Exception as e:
            print(f"更新背景时出错: {e}")
            import traceback
            traceback.print_exc()
            self.ui.update_background(None)  # 出错时清除背景
    
    def on_window_resize(self, event):
        """处理窗口大小变化"""
        if event.widget == self.window and event.width > 0 and event.height > 0:
            print(f"窗口大小变化: {event.width}x{event.height}")
            
            # 取消之前的延迟更新
            if self.resize_after_id:
                self.window.after_cancel(self.resize_after_id)
            
            # 设置新的延迟更新
            self.resize_after_id = self.window.after(100, self.update_background)
    
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
