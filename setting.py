"""设置管理模块"""
import os
import json
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from config import SETTINGS_FILE, DEFAULT_SETTINGS

class SettingsManager:
    def __init__(self):
        self.settings = self.load_settings()
    
    def load_settings(self):
        """加载设置"""
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return DEFAULT_SETTINGS.copy()
        except:
            return DEFAULT_SETTINGS.copy()
    
    def save_settings(self, settings):
        """保存设置"""
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f)
            self.settings = settings
            return True
        except:
            return False

class SettingsWindow:
    def __init__(self, parent, settings_manager, apply_callback):
        self.parent = parent
        self.settings_manager = settings_manager
        self.apply_callback = apply_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("设置")
        self.window.geometry("300x200")
        self.window.resizable(False, False)
        self.window.transient(parent)
        
        self.create_ui()
        self.load_current_settings()
    
    def create_ui(self):
        """创建设置窗口UI"""
        ttk.Label(self.window, text="背景设置", font=('Segoe UI', 12, 'bold')).pack(pady=10)
        
        # 背景图片选择
        bg_frame = ttk.Frame(self.window)
        bg_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(bg_frame, text="背景图片:").pack(side='left')
        self.bg_path_var = tk.StringVar()
        ttk.Entry(bg_frame, textvariable=self.bg_path_var, state='readonly').pack(side='left', fill='x', expand=True, padx=5)
        ttk.Button(bg_frame, text="浏览", command=self.select_background).pack(side='right')
        
        # 透明度调节
        alpha_frame = ttk.Frame(self.window)
        alpha_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(alpha_frame, text="透明度:").pack(side='left')
        self.alpha_var = tk.IntVar(value=100)
        self.alpha_scale = ttk.Scale(alpha_frame, from_=0, to=100, variable=self.alpha_var, orient='horizontal')
        self.alpha_scale.pack(side='left', fill='x', expand=True, padx=5)
        
        # 保存按钮
        ttk.Button(self.window, text="保存设置", command=self.save_settings).pack(pady=20)
    
    def load_current_settings(self):
        """加载当前设置"""
        settings = self.settings_manager.settings
        if os.path.exists(settings.get('background_path', '')):
            self.bg_path_var.set(settings['background_path'])
        self.alpha_var.set(settings.get('alpha', 100))
    
    def select_background(self):
        """选择背景图片"""
        file_path = filedialog.askopenfilename(
            title="选择背景图片",
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            self.bg_path_var.set(file_path)
            self.apply_settings()
    
    def save_settings(self):
        """保存设置"""
        settings = {
            'background_path': self.bg_path_var.get(),
            'alpha': self.alpha_var.get()
        }
        if self.settings_manager.save_settings(settings):
            self.apply_settings()
            self.window.destroy()
    
    def apply_settings(self):
        """应用设置"""
        settings = {
            'background_path': self.bg_path_var.get(),
            'alpha': self.alpha_var.get()
        }
        self.apply_callback(settings)
