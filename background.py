import os
import json
from tkinter import filedialog
from PIL import Image, ImageTk

class BackgroundManager:
    def __init__(self):
        self.current_background = None
        self.background_image = None
        self.config_file = "background_config.json"
        self.load_config()
    
    def load_config(self):
        """加载背景配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    if 'background' in config:
                        self.load_background(config['background'])
        except:
            pass
    
    def save_config(self):
        """保存背景配置"""
        config = {
            'background': self.current_background if self.current_background else ""
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except:
            pass
    
    def select_background(self):
        """选择背景图片"""
        file_path = filedialog.askopenfilename(
            title="选择背景图片",
            filetypes=[
                ("图片文件", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.load_background(file_path)
            self.save_config()
            return True
        return False
    
    def load_background(self, image_path):
        """加载背景图片"""
        try:
            if image_path and os.path.exists(image_path):
                # 保存当前背景路径
                self.current_background = image_path
                # 加载图片
                image = Image.open(image_path)
                return True
        except:
            self.current_background = None
        return False
    
    def clear_background(self):
        """清除背景"""
        self.current_background = None
        self.background_image = None
        self.save_config()
    
    def get_background(self, width, height):
        """获取适配大小的背景图片
        
        Args:
            width: 需要的宽度
            height: 需要的高度
            
        Returns:
            ImageTk.PhotoImage 对象或 None
        """
        try:
            if self.current_background and os.path.exists(self.current_background):
                # 加载原始图片
                image = Image.open(self.current_background)
                # 计算缩放比例
                img_width, img_height = image.size
                scale = max(width/img_width, height/img_height)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                # 缩放图片
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                # 裁剪到目标大小
                left = (new_width - width) // 2
                top = (new_height - height) // 2
                image = image.crop((left, top, left + width, top + height))
                # 转换为PhotoImage
                self.background_image = ImageTk.PhotoImage(image)
                return self.background_image
        except:
            pass
        return None
