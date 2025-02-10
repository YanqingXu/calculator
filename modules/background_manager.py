"""背景管理器模块"""
from PySide2.QtWidgets import (QFileDialog, QDialog, QVBoxLayout, QPushButton, 
                            QLabel, QSlider, QHBoxLayout)
from PySide2.QtCore import Qt
from PIL import Image
import json
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackgroundManager:
    """背景管理器类"""
    def __init__(self):
        self.callback = None
        self.current_background = None
        self.settings_file = "background_config.json"
        self.opacity = 0.8  # 默认透明度
        self.dialog = None
        self.load_settings()
    
    def set_callback(self, callback):
        """设置回调函数"""
        self.callback = callback
        if self.current_background:
            self.apply_background()
    
    def load_settings(self):
        """加载设置"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    bg_path = settings.get('background')
                    self.opacity = settings.get('opacity', 0.8)
                    if bg_path and os.path.exists(bg_path):
                        try:
                            self.current_background = Image.open(bg_path)
                        except Exception as e:
                            logger.error(f"无法加载背景图片 {bg_path}: {str(e)}")
                            self.current_background = None
        except Exception as e:
            logger.error(f"加载设置文件时出错: {str(e)}")
    
    def save_settings(self):
        """保存设置"""
        try:
            settings = {
                'background': str(self.current_background.filename) if self.current_background else None,
                'opacity': self.opacity
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存设置文件时出错: {str(e)}")
    
    def show_settings(self, parent=None):
        """显示设置对话框"""
        if not self.dialog:
            self.dialog = QDialog(parent)
            self.dialog.setWindowTitle("设置")
            self.dialog.setMinimumSize(300, 200)
            
            # 设置样式
            self.dialog.setStyleSheet("""
                QDialog {
                    background-color: rgba(255, 255, 255, 240);
                }
                QPushButton {
                    background-color: rgba(255, 255, 255, 180);
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 8px 16px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: rgba(240, 240, 240, 180);
                }
                QLabel {
                    color: #666;
                    padding: 5px;
                }
                QSlider {
                    margin: 10px;
                }
                QSlider::groove:horizontal {
                    border: 1px solid #999999;
                    height: 8px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
                    margin: 2px 0;
                }
                QSlider::handle:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                    border: 1px solid #5c5c5c;
                    width: 18px;
                    margin: -2px 0;
                    border-radius: 3px;
                }
            """)
            
            # 创建布局
            layout = QVBoxLayout(self.dialog)
            
            # 添加标题
            title = QLabel("背景设置")
            title.setAlignment(Qt.AlignCenter)
            layout.addWidget(title)
            
            # 添加按钮
            button_layout = QHBoxLayout()
            
            choose_bg_btn = QPushButton("设置背景")
            choose_bg_btn.clicked.connect(self.choose_background)
            button_layout.addWidget(choose_bg_btn)
            
            clear_bg_btn = QPushButton("清除背景")
            clear_bg_btn.clicked.connect(self.clear_background)
            button_layout.addWidget(clear_bg_btn)
            
            layout.addLayout(button_layout)
            
            # 添加透明度控制
            opacity_label = QLabel("背景透明度")
            opacity_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(opacity_label)
            
            self.opacity_slider = QSlider(Qt.Horizontal)
            self.opacity_slider.setMinimum(0)
            self.opacity_slider.setMaximum(100)
            self.opacity_slider.setValue(int(self.opacity * 100))
            self.opacity_slider.valueChanged.connect(self.opacity_changed)
            layout.addWidget(self.opacity_slider)
            
            # 添加关闭按钮
            close_button = QPushButton("关闭")
            close_button.clicked.connect(self.dialog.close)
            layout.addWidget(close_button)
        
        self.dialog.show()
    
    def opacity_changed(self, value):
        """处理透明度变化"""
        self.opacity = value / 100
        self.apply_background()
        self.save_settings()
    
    def choose_background(self):
        """选择背景图片"""
        file_name, _ = QFileDialog.getOpenFileName(
            self.dialog, "选择背景图片",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_name:
            try:
                self.current_background = Image.open(file_name)
                self.apply_background()
                self.save_settings()
            except Exception as e:
                logger.error(f"无法加载背景图片 {file_name}: {str(e)}")
    
    def clear_background(self):
        """清除背景"""
        self.current_background = None
        if self.callback:
            self.callback(None)
        self.save_settings()
    
    def apply_background(self):
        """应用背景"""
        if self.callback and self.current_background:
            # 创建半透明背景
            background = self.current_background.copy()
            if background.mode in ('RGBA', 'LA') or (background.mode == 'P' and 'transparency' in background.info):
                background.putalpha(int(255 * self.opacity))
            else:
                background = background.convert('RGBA')
                background.putalpha(int(255 * self.opacity))
            self.callback(background)
    
    def get_background(self, width, height):
        """获取调整大小后的背景图片"""
        if self.current_background:
            # 调整图片大小以适应窗口
            background = self.current_background.copy()
            background.thumbnail((width * 2, height * 2), Image.Resampling.LANCZOS)
            
            # 创建半透明背景
            if background.mode in ('RGBA', 'LA') or (background.mode == 'P' and 'transparency' in background.info):
                background.putalpha(int(255 * self.opacity))
            else:
                background = background.convert('RGBA')
                background.putalpha(int(255 * self.opacity))
            
            return background
        return None
