"""计算器核心逻辑模块"""
import math

class CalculatorCore:
    """计算器核心类"""
    def __init__(self):
        self.reset()
        self.memory = 0
        self.has_memory = False
    
    def reset(self):
        """重置计算器状态"""
        self.current_num = ""
        self.previous_num = None
        self.operation = None
        self.result = ""
        self.new_number = True
        self.decimal_pressed = False
    
    def clear_entry(self):
        """清除当前输入"""
        self.current_num = "0"
        self.new_number = True
        self.decimal_pressed = False
        return self.format_number(self.current_num)
    
    def clear_all(self):
        """清除所有内容"""
        self.reset()
        return self.format_number(self.current_num)
    
    def backspace(self):
        """退格"""
        if len(self.current_num) > 1:
            if self.current_num[-1] == '.':
                self.decimal_pressed = False
            self.current_num = self.current_num[:-1]
        else:
            self.current_num = "0"
            self.new_number = True
        return self.format_number(self.current_num)
    
    def number_press(self, num):
        """处理数字按键"""
        if self.new_number:
            self.current_num = str(num)
            self.new_number = False
        else:
            self.current_num += str(num)
        return self.format_number(self.current_num)
    
    def decimal_press(self):
        """处理小数点按键"""
        if not self.decimal_pressed:
            if self.new_number:
                self.current_num = "0."
                self.new_number = False
            else:
                self.current_num += "."
            self.decimal_pressed = True
        return self.current_num
    
    def operation_press(self, op):
        """处理运算符按键"""
        if self.previous_num is not None and not self.new_number:
            self.calculate()
        self.previous_num = float(self.current_num)
        self.operation = op
        self.new_number = True
        self.decimal_pressed = False
        return self.current_num
    
    def calculate(self):
        """执行计算"""
        if self.previous_num is not None and self.operation:
            try:
                current = float(self.current_num)
                if self.operation == '+':
                    result = self.previous_num + current
                elif self.operation == '-':
                    result = self.previous_num - current
                elif self.operation == '×':
                    result = self.previous_num * current
                elif self.operation == '÷':
                    if current == 0:
                        return "除数不能为零"
                    result = self.previous_num / current
                
                self.result = self.format_number(result)
                self.current_num = self.result
                self.previous_num = None
                self.operation = None
                self.new_number = True
                self.decimal_pressed = '.' in self.result
                
                return self.result
            except:
                return "错误"
        return self.format_number(self.current_num)
    
    def special_operation(self, op):
        """处理特殊运算"""
        try:
            num = float(self.current_num)
            
            if op == '%':
                # 如果在运算过程中按下%，将当前数作为百分比计算
                if self.previous_num is not None and self.operation:
                    percent_value = num / 100
                    if self.operation == '+' or self.operation == '-':
                        # 加减法中，百分比相对于第一个数计算
                        result = self.previous_num * percent_value
                    else:
                        # 乘除法中，直接用百分比值计算
                        result = percent_value
                else:
                    # 单独使用%时，计算百分比值
                    result = num / 100
            
            elif op == '±':
                result = -num
            
            elif op == 'x²':
                result = num * num
            
            elif op == '√':
                if num < 0:
                    return "无效输入"
                result = math.sqrt(num)
            
            elif op == '1/x':
                if num == 0:
                    return "除数不能为零"
                result = 1 / num
            
            # 格式化结果
            self.result = self.format_number(result)
            self.current_num = self.result
            self.new_number = True
            self.decimal_pressed = '.' in self.result
            
            # 如果在运算过程中使用特殊运算，更新当前数
            if self.previous_num is not None and self.operation and op == '%':
                self.current_num = self.result
                # 继续之前的运算
                return self.calculate()
            
            return self.result
        except:
            return "错误"
    
    def memory_operation(self, op):
        """处理内存操作"""
        if op == 'MC':  # Memory Clear
            self.memory = 0
            self.has_memory = False
        elif op == 'MR':  # Memory Recall
            self.current_num = str(self.memory)
            self.new_number = True
        elif op == 'M+':  # Memory Add
            self.memory += float(self.current_num)
            self.has_memory = True
            self.new_number = True
        elif op == 'M-':  # Memory Subtract
            self.memory -= float(self.current_num)
            self.has_memory = True
            self.new_number = True
        elif op == 'MS':  # Memory Store
            self.memory = float(self.current_num)
            self.has_memory = True
            self.new_number = True
        
        return self.format_number(self.current_num)
    
    def format_number(self, num):
        """格式化数字，整数不显示小数点，小数保留合适的精度"""
        try:
            # 如果是错误消息，直接返回
            if isinstance(num, str) and not num.replace('.', '').isdigit():
                return num
            
            # 转换为浮点数
            float_num = float(num)
            
            # 如果是整数，返回整数字符串
            if float_num.is_integer():
                return str(int(float_num))
            
            # 处理小数，去除尾部多余的0
            str_num = f"{float_num:.12g}"
            
            # 如果数字很大或很小，使用科学计数法
            if 'e' in str_num:
                return str_num
            
            return str_num
        except:
            return str(num)
