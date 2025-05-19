# src/interpreter.py
from parser import PrintNode, StringNode, NumberNode, VariableNode, AssignNode, BinaryOpNode, BooleanNode, IfNode

# Environment to store variables
environment = {}

def format_value_for_output(value):
    """Format value for output, converting booleans to Hebrew."""
    # Add RTL mark to ensure proper text direction
    rtl_mark = "\u200F"
    
    if isinstance(value, bool):
        return f"{rtl_mark}אמת" if value else f"{rtl_mark}שקר"
    elif isinstance(value, str):
        # For strings, add RTL mark
        return f"{rtl_mark}{value}"
    else:
        return f"{rtl_mark}{value}"

def evaluate_node(node):
    if isinstance(node, NumberNode):
        return node.value
    elif isinstance(node, StringNode):
        return node.value # Strings evaluate to their content
    elif isinstance(node, BooleanNode):
        return node.value # Boolean values (True or False)
    elif isinstance(node, VariableNode):
        var_name = node.name
        if var_name in environment:
            return environment[var_name]
        else:
            raise RuntimeError(f"Undefined variable: {var_name}")
    elif isinstance(node, BinaryOpNode):
        left_val = evaluate_node(node.left)
        right_val = evaluate_node(node.right)

        # Handle comparison operators
        if node.op.type == "EQUALS":
            return left_val == right_val
        elif node.op.type == "NOT_EQUALS":
            return left_val != right_val
        elif node.op.type == "LT":
            return left_val < right_val
        elif node.op.type == "GT":
            return left_val > right_val
        elif node.op.type == "LE":
            return left_val <= right_val
        elif node.op.type == "GE":
            return left_val >= right_val
            
        # For arithmetic operators, check that operands are numeric
        if node.op.type == "PLUS":
            # Handle string concatenation
            if isinstance(left_val, str) or isinstance(right_val, str):
                return str(left_val) + str(right_val)
            return left_val + right_val
        elif node.op.type == "MINUS":
            if not (isinstance(left_val, (int, float)) and isinstance(right_val, (int, float))):
                raise RuntimeError(f"The '-' operator requires numeric operands, got {type(left_val)} and {type(right_val)}")
            return left_val - right_val
        elif node.op.type == "MULTIPLY":
            # Allow string * number for repetition
            if isinstance(left_val, str) and isinstance(right_val, (int, float)):
                return left_val * int(right_val)
            elif isinstance(right_val, str) and isinstance(left_val, (int, float)):
                return right_val * int(left_val)
            elif not (isinstance(left_val, (int, float)) and isinstance(right_val, (int, float))):
                raise RuntimeError(f"The '*' operator requires numeric operands or string*number, got {type(left_val)} and {type(right_val)}")
            return left_val * right_val
        elif node.op.type == "DIVIDE":
            if not (isinstance(left_val, (int, float)) and isinstance(right_val, (int, float))):
                raise RuntimeError(f"The '/' operator requires numeric operands, got {type(left_val)} and {type(right_val)}")
            if right_val == 0:
                raise RuntimeError("Division by zero")
            return left_val / right_val # Using true division
        else:
            raise RuntimeError(f"Unknown binary operator: {node.op.type}")
    else:
        raise RuntimeError(f"Cannot evaluate node type: {type(node)}")

def interpret(ast_nodes):
    result = None
    i = 0
    while i < len(ast_nodes):
        node = ast_nodes[i]
        
        if isinstance(node, PrintNode):
            value_to_print = evaluate_node(node.value_node)
            formatted_value = format_value_for_output(value_to_print)
            
            # Handle Hebrew strings by printing as raw values
            if isinstance(formatted_value, str):
                print(formatted_value)
            else:
                print(formatted_value)
                
            result = value_to_print

        elif isinstance(node, AssignNode):
            var_name = node.variable_node.name
            value_to_assign = evaluate_node(node.value_node)
            environment[var_name] = value_to_assign
            result = value_to_assign
            
        elif isinstance(node, IfNode):
            condition_result = evaluate_node(node.condition)
            
            if condition_result:
                # Execute the if block
                if node.body:
                    # Interpret all statements in the if block
                    interpret(node.body)
            elif node.else_body:
                # Execute the else block if condition is false and there is an else block
                interpret(node.else_body)
        
        # BinaryOpNodes are handled by evaluate_node, direct interpretation isn't needed at top level
        # unless the language allows expressions as standalone statements (which Aron doesn't yet).

        else:
            raise RuntimeError(f"Unknown AST node type at top level: {type(node)}")
            
        i += 1
    
    return result

if __name__ == '__main__':
    from lexer import tokenize 
    from parser import parse   
    
    sample_codes = {
        "arithmetic_and_vars": """
# הגדרת משתנים
קבע א = 10
קבע ב = 25
קבע תוצאה = א + ב * 2 # 10 + 50 = 60
הדפס "תוצאה (א + ב * 2):"
הדפס תוצאה

# עם סוגריים
קבע ג = (תוצאה - 10) / 5 # (60 - 10) / 5 = 50 / 5 = 10
הדפס "ג ((תוצאה - 10) / 5):"
הדפס ג

הדפס "הדפסת ביטוי ישירות:"
הדפס 100 + 20 / 4 - 1 # 100 + 5 - 1 = 104
הדפס (100 + 20) / 4 - 1 # (100 + 20) / 4 - 1 = 120 / 4 - 1 = 30 - 1 = 29
""",
        "string_concat": """
קבע שם_פרטי = "אהרן"
קבע שם_משפחה = "הכהן"
קבע שם_מלא = שם_פרטי + " " + שם_משפחה
הדפס "שם מלא:"
הדפס שם_מלא
הדפס "חיבור ישיר: " + "עובד!" 
""",
        "boolean_and_conditions": """
קבע אמיתי = אמת
קבע שקרי = שקר
הדפס "ערכים בוליאנים:"
הדפס אמיתי
הדפס שקרי

הדפס "השוואות:"
הדפס 5 > 3  # אמת
הדפס 5 == 3 # שקר
הדפס 5 != 3 # אמת
הדפס 5 >= 5 # אמת
""",
        "if_else_tests": """
קבע מספר = 10
אם מספר > 5
    הדפס "המספר גדול מ-5"
    קבע כפול = מספר * 2
    הדפס "הכפלה:"
    הדפס כפול
אחרת
    הדפס "המספר קטן או שווה ל-5"
    קבע חצי = מספר / 2
    הדפס "חילוק לשניים:"
    הדפס חצי
סוף

קבע מספר_קטן = 3
אם מספר_קטן > 5
    הדפס "המספר גדול מ-5"
אחרת
    הדפס "המספר קטן או שווה ל-5"
    קבע חישוב = מספר_קטן * 3 - 1
    הדפס "חישוב מורכב:"
    הדפס חישוב
סוף

קבע בוליאני = אמת
אם בוליאני == אמת
    הדפס "בוליאני הוא אמת"
אחרת
    הדפס "בוליאני הוא שקר"
סוף

קבע בוליאני_שני = שקר
אם בוליאני_שני == אמת
    הדפס "בוליאני_שני הוא אמת"
אחרת
    הדפס "בוליאני_שני הוא שקר"
סוף
"""
    }

    for name, sample_code in sample_codes.items():
        print(f"--- Interpreting: {name} ---")
        print(f"Code:\n{sample_code}")
        
        environment.clear() # Clear environment for each test case
        tokens = tokenize(sample_code)
        
        try:
            ast = parse(tokens)
            interpret(ast)
        except RuntimeError as e:
            print(f"Runtime Error: {e}")
        except SyntaxError as e:
            print(f"Syntax Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        print("-" * 20 + "\n")
