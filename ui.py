"""计算器的UI相关模块"""
import tkinter as tk
from tkinter import ttk
from config import *

class CalculatorUI:
    def __init__(self, window, button_callback, memory_callback, history_callback):
        self.window = window
        self.button_callback = button_callback
        self.memory_callback = memory_callback
        self.history_callback = history_callback
        
        # 创建样式
        self.style = ttk.Style()
        self.style.configure('Calculator.TFrame', background='white')
        self.style.configure('Calculator.TButton', **BUTTON_STYLE)
        self.style.configure('Calculator.TLabel', background='white')
        self.style.configure('Calculator.TEntry', background='white')
        
        # 创建主容器
        self.container = ttk.Frame(window, style='Calculator.TFrame')
        self.container.place(relwidth=1, relheight=1)
        
        # 创建标题栏
        self.create_title_bar()
        
        # 创建显示区域
        self.create_display()
        
        # 创建按钮区域
        self.create_buttons()
    
    def create_title_bar(self):
        """创建标题栏"""
        title_frame = ttk.Frame(self.container, style='Calculator.TFrame')
        title_frame.pack(fill='x', padx=5, pady=2)
        
        # 左侧菜单按钮
        menu_button = ttk.Button(title_frame, text="≡", width=3)
        menu_button.pack(side='left')
        
        # 标题
        ttk.Label(title_frame, text="标准", style='Calculator.TLabel').pack(side='left', padx=10)
        
        # 历史按钮
        history_button = ttk.Button(title_frame, text="⟳", width=3,
                                  command=self.history_callback)
        history_button.pack(side='right')
    
    def create_display(self):
        """创建显示区域"""
        display_frame = ttk.Frame(self.container, style='Calculator.TFrame')
        display_frame.pack(fill='x', padx=5, pady=5)
        
        # 算式显示标签
        self.expression_label = ttk.Label(
            display_frame,
            text="",
            style='Calculator.TLabel',
            font=('Arial', 14),
            anchor='e'
        )
        self.expression_label.pack(fill='x', padx=5)
        
        # 结果显示框
        self.display_var = tk.StringVar(value="")  # 初始为空
        self.display = ttk.Entry(
            display_frame,
            textvariable=self.display_var,
            justify='right',
            font=('Arial', 24, 'bold'),
            state='readonly'
        )
        self.display.pack(fill='x', padx=5, pady=5)
    
    def create_buttons(self):
        """创建按钮区域"""
        button_frame = ttk.Frame(self.container, style='Calculator.TFrame')
        button_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # 内存按钮行
        memory_frame = ttk.Frame(button_frame, style='Calculator.TFrame')
        memory_frame.pack(fill='x', pady=1)
        for text in MEMORY_BUTTONS:
            btn = ttk.Button(memory_frame, text=text, style='Calculator.TButton')
            btn.pack(side='left', expand=True, padx=1)
            if text != 'M▾':  # M▾ 是下拉按钮，不需要绑定内存回调
                btn.bind('<Button-1>', lambda e, t=text: self.memory_callback(t))
        
        # 第一行功能按钮
        func_frame1 = ttk.Frame(button_frame, style='Calculator.TFrame')
        func_frame1.pack(fill='x', pady=1)
        for text in FUNCTION_ROW1:
            btn = ttk.Button(func_frame1, text=text, style='Calculator.TButton',
                           command=lambda t=text: self.button_callback(t))
            btn.pack(side='left', expand=True, padx=1)
        
        # 第二行功能按钮
        func_frame2 = ttk.Frame(button_frame, style='Calculator.TFrame')
        func_frame2.pack(fill='x', pady=1)
        for text in FUNCTION_ROW2:
            btn = ttk.Button(func_frame2, text=text, style='Calculator.TButton',
                           command=lambda t=text: self.button_callback(t))
            btn.pack(side='left', expand=True, padx=1)
        
        # 数字和运算符按钮
        for row in NUMBER_AND_OPERATORS:
            row_frame = ttk.Frame(button_frame, style='Calculator.TFrame')
            row_frame.pack(fill='x', pady=1)
            for text in row:
                btn = ttk.Button(row_frame, text=text, style='Calculator.TButton',
                               command=lambda t=text: self.button_callback(t))
                btn.pack(side='left', expand=True, padx=1)
    
    def update_display(self, expression, result, show_equals=False):
        """更新显示内容
        
        Args:
            expression: 要显示的表达式
            result: 计算结果
            show_equals: 是否显示等号（按下=时为True）
        """
        # 更新算式显示
        if expression:
            if show_equals:
                self.expression_label.config(text=expression + " =")
            else:
                self.expression_label.config(text=expression)
        else:
            self.expression_label.config(text="")
        
        # 更新结果显示
        self.display_var.set(result)
