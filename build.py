"""打包脚本"""
import os
import sys
import PyInstaller.__main__

def build():
    """打包应用"""
    # 获取图标路径
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
    
    # PyInstaller参数
    args = [
        'main.py',  # 主程序文件
        '--name=Calculator',  # 生成的exe名称
        '--windowed',  # 使用GUI模式
        '--onefile',  # 打包成单个文件
        '--clean',  # 清理临时文件
        '--noconfirm',  # 不确认覆盖
        '--add-data=modules;modules',  # 添加模块目录
    ]
    
    # 如果存在图标文件，添加图标
    if os.path.exists(icon_path):
        args.append(f'--icon={icon_path}')
    
    # 运行PyInstaller
    PyInstaller.__main__.run(args)

if __name__ == '__main__':
    build()
