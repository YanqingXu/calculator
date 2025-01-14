"""计算器的核心逻辑模块"""

class CalculatorLogic:
    def __init__(self):
        self.reset()
    
    def reset(self):
        """重置计算器状态"""
        self.current_number = "0"  # 当前输入的数字
        self.current_operator = ""  # 当前运算符
        self.previous_number = ""  # 上一个数字
        self.current_expression = "0"  # 当前完整表达式
        self.new_number = True  # 是否开始输入新数字
        self.has_decimal = False  # 是否已有小数点
        self.memory_value = "0"  # 初始化内存值
    
    def handle_number(self, number):
        """处理数字输入"""
        if self.new_number:
            # 如果是新数字且没有运算符，说明是新的计算
            if not self.current_operator:
                self.current_expression = number
            self.current_number = number
            self.new_number = False
        else:
            if len(self.current_number) < 16:  # 限制数字长度
                self.current_number += number
        
        # 更新表达式
        if self.previous_number and self.current_operator:
            self.current_expression = f"{self.previous_number} {self.current_operator} {self.current_number}"
        else:
            self.current_expression = self.current_number
        
        return None  # 不返回结果，只在计算完成时返回
    
    def handle_decimal(self):
        """处理小数点输入"""
        if self.new_number:
            # 如果是新数字且没有运算符，说明是新的计算
            if not self.current_operator:
                self.current_expression = "0."
            self.current_number = "0."
            self.new_number = False
        elif not self.has_decimal:
            self.current_number += "."
        
        self.has_decimal = True
        
        # 更新表达式
        if self.previous_number and self.current_operator:
            self.current_expression = f"{self.previous_number} {self.current_operator} {self.current_number}"
        else:
            self.current_expression = self.current_number
        
        return None  # 不返回结果，只在计算完成时返回
    
    def handle_operator(self, operator):
        """处理运算符输入"""
        if self.current_operator and not self.new_number:
            # 如果已经有运算符且正在输入第二个数，先计算
            result = self.calculate()
            if result == "错误":
                return result
        
        # 保存当前数字作为第一个操作数
        self.previous_number = self.current_number
        self.current_operator = operator
        self.new_number = True
        self.has_decimal = False
        
        # 更新表达式
        self.current_expression = f"{self.previous_number} {operator}"
        
        return None  # 不返回结果，只在计算完成时返回
    
    def calculate(self):
        """执行计算"""
        if not self.current_operator or self.new_number:
            return self.current_number
        
        try:
            num1 = float(self.previous_number)
            num2 = float(self.current_number)
            
            if self.current_operator == "+":
                result = num1 + num2
            elif self.current_operator == "-":
                result = num1 - num2
            elif self.current_operator == "×":
                result = num1 * num2
            elif self.current_operator == "÷":
                if num2 == 0:
                    return "错误"
                result = num1 / num2
            
            # 格式化结果
            if result.is_integer():
                result_str = str(int(result))
            else:
                result_str = "{:.10f}".format(result).rstrip("0").rstrip(".")
            
            # 保存当前表达式用于显示
            self.current_expression = f"{self.previous_number} {self.current_operator} {self.current_number}"
            
            # 更新计算器状态，保持结果作为下一次计算的起始值
            self.current_number = result_str
            self.previous_number = ""
            self.current_operator = ""
            self.new_number = False  # 改为 False，这样结果可以用于下一次计算
            self.has_decimal = "." in result_str
            
            return result_str
            
        except:
            return "错误"
    
    def handle_memory(self, operation):
        """处理内存操作
        
        Args:
            operation: 内存操作类型 ('MC', 'MR', 'MS', 'M+', 'M-')
        
        Returns:
            如果是MR操作，返回内存值；否则返回None
        """
        try:
            if operation == 'MC':  # Memory Clear
                self.memory_value = "0"
                return None
                
            elif operation == 'MR':  # Memory Recall
                self.current_number = self.memory_value
                self.new_number = False
                if not self.current_operator:
                    self.current_expression = self.memory_value
                else:
                    self.current_expression = f"{self.previous_number} {self.current_operator} {self.memory_value}"
                return self.memory_value
                
            elif operation == 'MS':  # Memory Store
                self.memory_value = self.current_number
                return None
                
            elif operation == 'M+':  # Memory Add
                memory = float(self.memory_value)
                current = float(self.current_number)
                result = memory + current
                if result.is_integer():
                    self.memory_value = str(int(result))
                else:
                    self.memory_value = "{:.10f}".format(result).rstrip("0").rstrip(".")
                return None
                
            elif operation == 'M-':  # Memory Subtract
                memory = float(self.memory_value)
                current = float(self.current_number)
                result = memory - current
                if result.is_integer():
                    self.memory_value = str(int(result))
                else:
                    self.memory_value = "{:.10f}".format(result).rstrip("0").rstrip(".")
                return None
                
        except:
            return "错误"
            
    def has_memory(self):
        """检查内存中是否有非零值"""
        try:
            return float(self.memory_value) != 0
        except:
            return False
    
    def clear_all(self):
        """清除所有内容"""
        self.reset()
        return "0"
    
    def clear_entry(self):
        """清除当前输入"""
        self.current_number = "0"
        self.new_number = True
        self.has_decimal = False
        
        # 更新表达式
        if self.previous_number and self.current_operator:
            self.current_expression = f"{self.previous_number} {self.current_operator}"
        else:
            self.current_expression = "0"
        
        return "0"
