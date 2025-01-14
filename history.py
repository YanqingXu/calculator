"""历史记录管理模块"""
import json
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class HistoryManager:
    def __init__(self, filename="calculator_history.json"):
        self.filename = filename
        self.history = self.load_history()
    
    def load_history(self):
        """加载历史记录"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def save_history(self):
        """保存历史记录"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add_calculation(self, expression, result):
        """添加计算记录"""
        # 创建历史记录项
        history_item = {
            'expression': expression,
            'result': result,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 添加到历史记录列表
        self.history.append(history_item)
        
        # 保持最多100条记录
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        # 保存到文件
        self.save_history()
    
    def clear_history(self):
        """清空历史记录"""
        self.history = []
        self.save_history()

class HistoryWindow:
    def __init__(self, parent, history_manager, select_callback):
        self.window = None
        self.parent = parent
        self.history_manager = history_manager
        self.select_callback = select_callback
    
    def show(self):
        """显示历史记录窗口"""
        if self.window:
            self.refresh_history()
            return
        
        # 创建窗口
        self.window = tk.Toplevel(self.parent)
        self.window.title("计算历史")
        self.window.geometry("300x400")
        self.window.transient(self.parent)
        
        # 创建样式
        style = ttk.Style()
        style.configure('History.TFrame', background='white')
        style.configure('History.TLabel', background='white')
        
        # 创建主容器
        container = ttk.Frame(self.window, style='History.TFrame')
        container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 创建标题栏
        title_frame = ttk.Frame(container, style='History.TFrame')
        title_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(
            title_frame,
            text="历史记录",
            style='History.TLabel',
            font=('Arial', 12, 'bold')
        ).pack(side='left')
        
        # 清除按钮
        ttk.Button(
            title_frame,
            text="清除历史",
            command=self.clear_history
        ).pack(side='right')
        
        # 创建滚动区域
        self.history_frame = ttk.Frame(container, style='History.TFrame')
        self.history_frame.pack(fill='both', expand=True)
        
        # 显示历史记录
        self.refresh_history()
        
        # 处理窗口关闭
        self.window.protocol("WM_DELETE_WINDOW", self.hide)
    
    def refresh_history(self):
        """刷新历史记录显示"""
        # 清除现有内容
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        # 显示历史记录
        for item in reversed(self.history_manager.history):
            # 创建记录项框架
            item_frame = ttk.Frame(self.history_frame, style='History.TFrame')
            item_frame.pack(fill='x', pady=2)
            item_frame.bind('<Button-1>', lambda e, i=item: self.select_callback(i))
            
            # 显示表达式和结果
            expression = item['expression']
            
            ttk.Label(
                item_frame,
                text=expression,
                style='History.TLabel',
                font=('Arial', 10),
                anchor='e'
            ).pack(fill='x')
            
            ttk.Label(
                item_frame,
                text=item['result'],
                style='History.TLabel',
                font=('Arial', 12, 'bold'),
                anchor='e'
            ).pack(fill='x')
            
            # 显示时间戳
            ttk.Label(
                item_frame,
                text=item['timestamp'],
                style='History.TLabel',
                font=('Arial', 8),
                foreground='gray'
            ).pack(fill='x')
            
            # 添加分隔线
            ttk.Separator(self.history_frame).pack(fill='x', pady=5)
    
    def clear_history(self):
        """清空历史记录"""
        self.history_manager.clear_history()
        self.refresh_history()
    
    def hide(self):
        """隐藏窗口"""
        if self.window:
            self.window.withdraw()
    
    def show_if_hidden(self):
        """如果窗口隐藏则显示"""
        if self.window and not self.window.winfo_viewable():
            self.window.deiconify()
            self.refresh_history()
