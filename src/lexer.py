# src/lexer.py
import re

class Token:
    def __init__(self, type, value, line=0, column=0):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line}, col={self.column})"

# Aron keywords
KEYWORDS = {
    "הדפס": "PRINT",  # Keyword for "print"
    "קבע": "ASSIGN_KW", # Keyword for "assign" / "set"
    "אם": "IF", # Keyword for "if"
    "אחרת": "ELSE", # Keyword for "else"
    "אמת": "TRUE", # Keyword for "true"
    "שקר": "FALSE", # Keyword for "false"
    "סוף": "END", # Keyword for "end" (to mark the end of blocks)
}

def tokenize(code):
    tokens = []
    lines = code.split('\n')
    current_line = 0

    for line_num, line in enumerate(lines):
        current_line = line_num + 1  # 1-based line numbering
        position = 0
        
        # Skip empty lines
        if not line.strip():
            continue
            
        while position < len(line):
            # Skip whitespace
            match = re.match(r'\s+', line[position:])
            if match:
                position += match.end()
                continue
                
            # Skip comments
            if line[position] == '#':
                break  # Skip the rest of the line
                
            # Check for string literals
            if line[position] == '"':
                # Find the closing quote
                start_pos = position
                position += 1  # Skip opening quote
                string_content = ""
                
                while position < len(line) and line[position] != '"':
                    # Handle escape sequences
                    if line[position] == '\\' and position + 1 < len(line):
                        position += 1
                        if line[position] == '"':
                            string_content += '"'
                        elif line[position] == '\\':
                            string_content += '\\'
                        elif line[position] == 'n':
                            string_content += '\n'
                        else:
                            string_content += '\\' + line[position]
                    else:
                        string_content += line[position]
                    position += 1
                    
                if position < len(line) and line[position] == '"':
                    position += 1  # Skip closing quote
                    tokens.append(Token("STRING", string_content, current_line, start_pos + 1))
                else:
                    raise RuntimeError(f"Unclosed string starting at line {current_line}, column {start_pos + 1}")
                continue
                
            # Check for operators and special tokens
            for pattern, token_type in [
                (r'==', "EQUALS"),
                (r'!=', "NOT_EQUALS"),
                (r'<=', "LE"),
                (r'>=', "GE"),
                (r'=', "ASSIGN_OP"),
                (r'<', "LT"),
                (r'>', "GT"),
                (r'\(', "LPAREN"),
                (r'\)', "RPAREN"),
                (r'\+', "PLUS"),
                (r'-', "MINUS"),
                (r'\*', "MULTIPLY"),
                (r'/', "DIVIDE"),
            ]:
                match = re.match(pattern, line[position:])
                if match:
                    tokens.append(Token(token_type, match.group(), current_line, position + 1))
                    position += match.end()
                    break
            else:
                # If no operator matched, check for identifiers or keywords
                match = re.match(r'[א-ת][א-ת0-9_]*', line[position:])
                if match:
                    identifier = match.group()
                    # Check if it's a keyword
                    if identifier in KEYWORDS:
                        tokens.append(Token(KEYWORDS[identifier], identifier, current_line, position + 1))
                    else:
                        tokens.append(Token("IDENTIFIER", identifier, current_line, position + 1))
                    position += match.end()
                    continue
                    
                # Check for numbers
                match = re.match(r'\d+(\.\d+)?', line[position:])
                if match:
                    number_str = match.group()
                    if '.' in number_str:
                        value = float(number_str)
                    else:
                        value = int(number_str)
                    tokens.append(Token("NUMBER", value, current_line, position + 1))
                    position += match.end()
                    continue
                    
                # If nothing matched, it's an unexpected character
                raise RuntimeError(f"Unexpected character '{line[position]}' at line {current_line}, column {position + 1}")
                
    return tokens

if __name__ == '__main__':
    sample_code = '''
# זוהי הערה
קבע משתנה = "ערך כלשהו"
הדפס משתנה
הדפס "שלום עולם"
קבע א = 10
קבע ב = 20
קבע ג = (א + ב) * 2 # בדיקת סוגריים
הדפס ג
קבע בוליאני = אמת # ערך בוליאני
אם בוליאני == אמת
    הדפס "בוליאני הוא אמת"
אחרת
    הדפס "בוליאני הוא שקר"
סוף
    '''
    print(f"Tokenizing: {sample_code}")
    tokens = tokenize(sample_code)
    for token in tokens:
        print(token)
