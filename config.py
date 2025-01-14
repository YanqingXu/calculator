"""配置文件，存储常量和配置项"""

# 窗口配置
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 500
WINDOW_TITLE = "计算器"

# 样式配置
BUTTON_STYLE = {
    'font': ('Segoe UI', 12),
    'width': 5,
    'padding': 2
}

DISPLAY_STYLE = {
    'expression_font': ('Segoe UI', 12),
    'result_font': ('Segoe UI', 20, 'bold')
}

# 按钮布局配置
MEMORY_BUTTONS = ['MC', 'MR', 'M+', 'M-', 'MS', 'M▾']
FUNCTION_ROW1 = ['%', '√', 'x²', '1/x']
FUNCTION_ROW2 = ['CE', 'C', '⌫', '÷']
NUMBER_AND_OPERATORS = [
    ['7', '8', '9', '×'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['±', '0', '.', '=']
]

# 文件路径
SETTINGS_FILE = 'calculator_settings.json'

# 默认设置
DEFAULT_SETTINGS = {
    'background_path': '',
    'alpha': 100
}
