# Calculator with Custom Background

中文 | [English](README_EN.md)

一个基于Python和PySide2开发的现代化计算器应用，支持自定义背景图片功能。

## 功能特点

- 基本的数学运算（加、减、乘、除）
- 支持小数点运算
- 自定义背景图片设置
- 运算历史记录
- 键盘快捷键支持
- 现代化UI界面

## 技术栈

- Python 3.x
- PySide2 5.15.2.1 (Qt框架)
- Pillow 9.5.0 (图片处理)
- PyInstaller 5.13.2 (打包工具)

## 项目结构

```
calculator/
├── main.py              # 主程序入口
├── modules/             # 模块目录
│   ├── calculator_ui.py     # UI界面实现
│   ├── calculator_core.py   # 计算器核心逻辑
│   ├── background_manager.py# 背景管理器
│   ├── history_manager.py   # 历史记录管理
│   ├── keyboard_handler.py  # 键盘事件处理
│   └── base_widget.py       # 基础组件
├── requirements.txt     # 项目依赖
└── background_config.json # 背景配置文件
```

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/YanqingXu/calculator.git
cd calculator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行程序：
```bash
python main.py
```

## 使用说明

- 基本运算：直接点击数字和运算符按钮
- 键盘支持：可使用键盘输入数字和运算符
- 背景设置：点击设置按钮选择自定义背景图片
- 历史记录：可查看之前的计算历史

## 构建可执行文件

使用PyInstaller打包程序：
```bash
pyinstaller build.py
```

## 贡献指南

欢迎提交问题和改进建议！如果您想贡献代码：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件
