# src/parser.py
# Placeholder for the Parser
# A real parser would build an Abstract Syntax Tree (AST)

class ASTNode:
    pass

class PrintNode(ASTNode):
    def __init__(self, value_node):
        self.value_node = value_node

    def __repr__(self):
        return f"PrintNode({self.value_node})"

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value # The string literal itself, e.g., "Hello" (without quotes)

    def __repr__(self):
        return f"StringNode('{self.value}')"

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = int(value) # Store as integer

    def __repr__(self):
        return f"NumberNode({self.value})"

class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value  # True or False

    def __repr__(self):
        return f"BooleanNode({self.value})"

class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"VariableNode('{self.name}')"

class AssignNode(ASTNode):
    def __init__(self, variable_node, value_node):
        self.variable_node = variable_node
        self.value_node = value_node

    def __repr__(self):
        return f"AssignNode({self.variable_node}, {self.value_node})"

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op # Token (e.g., Token('PLUS', '+'))
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.left}, {self.op.type}, {self.right})"

class IfNode(ASTNode):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition  # Expression node
        self.body = body          # List of statement nodes for the if block
        self.else_body = else_body  # List of statement nodes for the else block, or None

    def __repr__(self):
        if self.else_body:
            return f"IfNode(condition={self.condition}, body={self.body}, else_body={self.else_body})"
        else:
            return f"IfNode(condition={self.condition}, body={self.body})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        if self.tokens and self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def consume(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        else:
            expected = token_type
            found = self.current_token.type if self.current_token else "End of Tokens"
            
            # Better error message with line and column information
            if self.current_token:
                line_info = f" at line {self.current_token.line}, column {self.current_token.column}"
            else:
                line_info = " at end of file"
                
            raise SyntaxError(f"Expected token {expected}, got {found}{line_info}")

    def parse_factor(self):
        token = self.current_token
        if token is None:
            raise SyntaxError(f"Unexpected end of input. Expected factor at pos {self.pos}.")
        
        if token.type == "NUMBER":
            self.advance()
            return NumberNode(token.value)
        elif token.type == "STRING": # Though strings usually don't participate in arithmetic directly
            self.advance()
            return StringNode(token.value[1:-1]) # Remove quotes
        elif token.type == "IDENTIFIER":
            self.advance()
            return VariableNode(token.value)
        elif token.type == "TRUE":
            self.advance()
            return BooleanNode(True)
        elif token.type == "FALSE":
            self.advance()
            return BooleanNode(False)
        elif token.type == "LPAREN":
            self.advance()  # Consume the '('
            expr = self.parse_expression()  # Parse the expression inside
            
            # Now we should find a closing parenthesis
            if self.current_token and self.current_token.type == "RPAREN":
                self.advance()  # Consume the ')'
                return expr
            else:
                raise SyntaxError(f"Expected ')', got {self.current_token.type if self.current_token else 'EOF'}")
        else:
            raise SyntaxError(f"Expected NUMBER, STRING, IDENTIFIER, TRUE, FALSE or LPAREN, got {token.type} ('{token.value}') at pos {self.pos}")

    def parse_term(self): # Handles * and /
        node = self.parse_factor()
        while self.current_token and self.current_token.type in ("MULTIPLY", "DIVIDE"):
            op_token = self.current_token
            self.advance()
            right_node = self.parse_factor()
            node = BinaryOpNode(node, op_token, right_node)
        return node

    def parse_expression(self): # Handles + and -
        node = self.parse_term()
        while self.current_token and self.current_token.type in ("PLUS", "MINUS"):
            op_token = self.current_token
            self.advance()
            right_node = self.parse_term()
            node = BinaryOpNode(node, op_token, right_node)
        return node
    
    def parse_comparison(self):
        expr = self.parse_expression()
        
        # Check if the next token is a comparison operator
        if self.current_token and self.current_token.type in ("EQUALS", "NOT_EQUALS", "LT", "GT", "LE", "GE"):
            op_token = self.current_token
            self.advance()
            right_expr = self.parse_expression()
            return BinaryOpNode(expr, op_token, right_expr)
        
        return expr

    def parse_statement(self):
        if self.current_token is None:
            return None # No more tokens

        if self.current_token.type == "PRINT":
            self.consume("PRINT")
            value_node = self.parse_comparison() # Use parse_comparison instead of parse_expression
            return PrintNode(value_node)

        elif self.current_token.type == "ASSIGN_KW": # קבע
            self.consume("ASSIGN_KW")
            var_name_token = self.consume("IDENTIFIER")
            variable_node = VariableNode(var_name_token.value)
            self.consume("ASSIGN_OP")
            value_node = self.parse_comparison() # Use parse_comparison instead of parse_expression
            return AssignNode(variable_node, value_node)
            
        elif self.current_token.type == "IF": # אם
            self.consume("IF")
            condition = self.parse_comparison()  # Parse the condition expression
            
            # Parse the body of the if statement (all statements until 'אחרת' or 'סוף')
            body = []
            while self.current_token and self.current_token.type not in ["ELSE", "END"]:
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
                else:
                    break
            
            # Check for 'אחרת' (else)
            else_body = None
            if self.current_token and self.current_token.type == "ELSE":
                self.consume("ELSE")
                else_body = []
                # Parse the body of the else statement (all statements until 'סוף')
                while self.current_token and self.current_token.type != "END":
                    stmt = self.parse_statement()
                    if stmt:
                        else_body.append(stmt)
                    else:
                        break
            
            # Expect 'סוף' (end) to close the if-else structure
            if self.current_token and self.current_token.type == "END":
                self.consume("END")
                return IfNode(condition, body, else_body)
            else:
                raise SyntaxError(f"Expected 'סוף' to close if-else block, got {self.current_token.type if self.current_token else 'EOF'}")
        else:
            raise SyntaxError(f"Unexpected token at start of statement: {self.current_token.type} ('{self.current_token.value}') at pos {self.pos}")

    def parse(self):
        ast_nodes = []
        while self.current_token: # Loop as long as there are tokens
            statement = self.parse_statement()
            if statement: # parse_statement might return None if no tokens
                ast_nodes.append(statement)
            else: # Should only happen if self.current_token became None inside loop unexpectedly
                break 
        return ast_nodes

# Global parse function to be called from outside
def parse(tokens):
    if not tokens:
        return []
    parser = Parser(tokens)
    return parser.parse()

if __name__ == '__main__':
    from lexer import tokenize # Assuming Token class is not directly needed for this test setup
    
    sample_codes = {
        "simple_arithmetic": """
            קבע תוצאה = 10 + 5 * 2 # Should be 20
            הדפס תוצאה
            קבע ערך_אחר = (100 - 10) / 3 # Will be 90/3 = 30
            הדפס ערך_אחר
        """,
        "variable_in_expression": """
            קבע א = 10
            קבע ב = 5
            קבע ג = א * ב + 2 # 50 + 2 = 52
            הדפס ג
        """,
        "parenthesis_test": """
            הדפס (7 + 3) * 4 # (7 + 3) * 4 = 10 * 4 = 40
            קבע א = (5 + 2) * (10 - 8) # (5 + 2) * (10 - 8) = 7 * 2 = 14
            הדפס א
        """,
        "boolean_test": """
            קבע אמיתי = אמת
            קבע שקרי = שקר
            הדפס אמיתי
            הדפס שקרי
        """,
        "if_else_test": """
            קבע מספר = 10
            אם מספר > 5
                הדפס "המספר גדול מ-5"
                קבע תוצאה = מספר * 2
                הדפס תוצאה
            אחרת
                הדפס "המספר קטן או שווה ל-5"
                קבע תוצאה = מספר / 2
                הדפס תוצאה
            סוף
            
            קבע בוליאני = אמת
            אם בוליאני == אמת
                הדפס "בוליאני הוא אמת"
            אחרת
                הדפס "בוליאני הוא שקר"
            סוף
        """
    }

    for name, sample_code in sample_codes.items():
        print(f"--- Testing: {name} ---")
        print(f"Code:\\n{sample_code}")
        tokens = tokenize(sample_code)
        print(f"Tokens: {tokens}")
        try:
            ast = parse(tokens)
            print(f"AST: {ast}")
        except Exception as e:
            print(f"Error during parsing: {e}")
        print("-" * 20 + "\\n")
