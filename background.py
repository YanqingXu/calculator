import os
import json
from tkinter import filedialog
from PIL import Image, ImageTk

class BackgroundManager:
    def __init__(self):
        self.current_background = None
        self.background_image = None  # 保持对PhotoImage的引用
        self.config_file = "background_config.json"
        self.load_config()
    
    def load_config(self):
        """加载背景配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    if 'background' in config and config['background']:
                        self.current_background = config['background']
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
            self.current_background = file_path
            self.save_config()
            return True
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
                print(f"加载背景图片: {self.current_background}")
                print(f"目标大小: {width}x{height}")
                
                # 加载原始图片
                image = Image.open(self.current_background)
                print(f"原始图片大小: {image.size}")
                
                # 计算缩放比例，保持宽高比
                img_width, img_height = image.size
                width_ratio = width / img_width
                height_ratio = height / img_height
                
                if width_ratio > height_ratio:
                    # 按宽度缩放
                    new_width = width
                    new_height = int(img_height * width_ratio)
                else:
                    # 按高度缩放
                    new_width = int(img_width * height_ratio)
                    new_height = height
                
                print(f"缩放后大小: {new_width}x{new_height}")
                
                # 缩放图片
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 居中裁剪
                left = (new_width - width) // 2
                top = (new_height - height) // 2
                right = left + width
                bottom = top + height
                
                print(f"裁剪区域: ({left}, {top}, {right}, {bottom})")
                image = image.crop((left, top, right, bottom))
                print(f"最终大小: {image.size}")
                
                # 转换为PhotoImage并保持引用
                self.background_image = ImageTk.PhotoImage(image)
                return self.background_image
                
        except Exception as e:
            print(f"加载背景图片错误: {e}")
            import traceback
            traceback.print_exc()
        return None
