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
    
    def handle_number(self, number):
        """处理数字输入"""
        if self.new_number:
            self.current_number = number
            self.new_number = False
            # 清除之前的表达式，因为要开始新的计算
            if not self.current_operator:
                self.current_expression = number
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
            self.current_number = "0."
            self.new_number = False
            # 清除之前的表达式，因为要开始新的计算
            if not self.current_operator:
                self.current_expression = "0."
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
                return None
            # 将结果作为第一个数
            self.previous_number = result
        elif not self.new_number or self.current_operator:
            # 如果正在输入第一个数或已经有运算符
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
            
            # 更新计算器状态
            self.current_number = result_str
            self.previous_number = ""
            self.current_operator = ""
            self.new_number = True
            self.has_decimal = "." in result_str
            
            return result_str
            
        except:
            return "错误"
    
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
