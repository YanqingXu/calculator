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
        
        # 配置样式
        self.style = ttk.Style()
        self.style.configure('Calculator.TFrame', background='white')
        self.style.configure('Calculator.TButton', **BUTTON_STYLE)
        self.style.configure('Calculator.TLabel', background='white')
        self.style.configure('Calculator.TEntry', background='white')
        
        # 内存按钮样式 - 无边框，悬停时显示背景色
        self.style.configure('Memory.TButton',
                           background='white',
                           borderwidth=0,
                           relief='flat',
                           font=('Arial', 10))
        self.style.map('Memory.TButton',
                      background=[('active', '#e6e6e6')])
        
        # 标题栏样式
        self.style.configure('Title.TButton',
                           background='white',
                           borderwidth=0,
                           relief='flat',
                           font=('Arial', 12))
        self.style.map('Title.TButton',
                      background=[('active', '#e6e6e6')])
        self.style.configure('Title.TLabel',
                           background='white')
        
        self.style.configure('MemoryIndicator.TLabel',
                           background='white',
                           font=('Arial', 10))
        
        # 创建主容器
        self.container = ttk.Frame(window, style='Calculator.TFrame')
        self.container.pack(fill='both', expand=True, padx=2, pady=2)
        
        # 创建背景画布
        self.background_canvas = tk.Canvas(
            self.container,
            highlightthickness=0,
            background='white'
        )
        self.background_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # 创建内容框架
        self.content_frame = ttk.Frame(
            self.container,
            style='Calculator.TFrame'
        )
        self.content_frame.place(relwidth=1, relheight=1)
        
        # 使所有框架透明
        self.style.configure('Calculator.TFrame', background='')
        self.style.configure('Calculator.TLabel', background='')
        self.style.configure('Memory.TButton', background='')
        self.style.configure('Title.TButton', background='')
        self.style.configure('Title.TLabel', background='')
        self.style.configure('MemoryIndicator.TLabel', background='')
        
        self.create_title_bar()
        self.create_display()
        self.create_buttons()
    
    def create_title_bar(self):
        """创建标题栏"""
        title_frame = ttk.Frame(self.content_frame, style='Calculator.TFrame')
        title_frame.pack(fill='x', padx=5, pady=2)
        
        # 设置按钮
        settings_btn = ttk.Button(
            title_frame,
            text="⚙",  # 使用齿轮图标
            style='Title.TButton',
            width=3,
            command=lambda: self.button_callback('settings')
        )
        settings_btn.pack(side='left')
        
        # 背景文字
        background_label = ttk.Label(
            title_frame,
            text="背景",
            style='Title.TLabel',
            font=('Arial', 16)
        )
        background_label.pack(side='left', padx=10)
        
        # 历史按钮
        history_button = ttk.Button(title_frame, text="⟳", width=3,
                                  command=self.history_callback)
        history_button.pack(side='right')
    
    def create_display(self):
        """创建显示区域"""
        display_frame = ttk.Frame(self.content_frame, style='Calculator.TFrame')
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
        # 内存按钮区域
        memory_frame = ttk.Frame(self.content_frame, style='Calculator.TFrame')
        memory_frame.pack(fill='x', padx=5)
        
        # 使用Grid布局来确保按钮均匀分布
        memory_frame.grid_columnconfigure((0,1,2,3,4,5), weight=1)  # 6个列等宽
        
        # 内存按钮
        memory_buttons = ['MC', 'MR', 'M+', 'M-', 'MS', 'M▾']
        for i, text in enumerate(memory_buttons):
            if text == 'M▾':  # 内存历史按钮
                btn = ttk.Label(
                    memory_frame,
                    text=text,
                    style='Memory.TButton',
                    cursor='hand2'  # 鼠标悬停时显示手型
                )
            else:
                btn = ttk.Button(
                    memory_frame,
                    text=text,
                    style='Memory.TButton',
                    command=lambda t=text: self.memory_callback(t)
                )
            btn.grid(row=0, column=i, sticky='nsew', padx=1, pady=5)
        
        # 添加内存指示器标签
        self.memory_indicator = ttk.Label(
            memory_frame,
            text="M",
            style='MemoryIndicator.TLabel'
        )
        self.memory_indicator.grid(row=0, column=6, padx=5)
        self.memory_indicator.grid_remove()  # 初始时隐藏
        
        # 添加分隔线
        separator = ttk.Separator(self.content_frame, orient='horizontal')
        separator.pack(fill='x', padx=5, pady=2)
        
        # 数字和运算符按钮区域
        buttons_frame = ttk.Frame(self.content_frame, style='Calculator.TFrame')
        buttons_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        button_texts = [
            ['%', 'CE', 'C', '⌫'],
            ['1/x', 'x²', '√', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]
        
        for row_texts in button_texts:
            row = ttk.Frame(buttons_frame, style='Calculator.TFrame')
            row.pack(fill='x', expand=True, pady=1)
            for text in row_texts:
                btn = ttk.Button(
                    row,
                    text=text,
                    style='Calculator.TButton',
                    width=5,
                    command=lambda t=text: self.button_callback(t)
                )
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
    
    def update_memory_indicator(self, has_memory):
        """更新内存指示器显示状态"""
        if has_memory:
            self.memory_indicator.grid()  # 使用grid而不是pack
        else:
            self.memory_indicator.grid_remove()
    
    def update_background(self, background_image):
        """更新背景图片"""
        print("更新背景图片")
        # 清除现有背景
        self.background_canvas.delete('all')
        
        if background_image:
            print("有背景图片")
            # 获取画布大小
            width = self.container.winfo_width()
            height = self.container.winfo_height()
            print(f"画布大小: {width}x{height}")
            
            try:
                # 创建背景图片
                image_id = self.background_canvas.create_image(
                    width // 2,  # 居中显示
                    height // 2,
                    image=background_image,
                    anchor='center'
                )
                print(f"创建背景图片成功，ID: {image_id}")
                
                # 确保内容框架在背景画布之上
                self.content_frame.lift()
                print("内容框架已提升到顶层")
                
                # 使所有框架透明
                self.style.configure('Calculator.TFrame', background='')
                self.style.configure('Calculator.TLabel', background='')
                self.style.configure('Memory.TButton', background='')
                self.style.configure('Title.TButton', background='')
                self.style.configure('Title.TLabel', background='')
                self.style.configure('MemoryIndicator.TLabel', background='')
            except Exception as e:
                print(f"创建背景图片时出错: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("无背景图片，恢复白色背景")
            # 恢复白色背景
            self.style.configure('Calculator.TFrame', background='white')
            self.style.configure('Calculator.TLabel', background='white')
            self.style.configure('Memory.TButton', background='white')
            self.style.configure('Title.TButton', background='white')
            self.style.configure('Title.TLabel', background='white')
            self.style.configure('MemoryIndicator.TLabel', background='white')
