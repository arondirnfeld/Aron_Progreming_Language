# rtl_formatter.py
# Module to format Aron code with proper RTL indentation

import re

def format_aron_code(code):
    """Format Aron code for better RTL display."""
    lines = code.split('\n')
    formatted_lines = []
    indent_level = 0
    
    # Keywords that increase indent
    indent_keywords = ['אם']
    # Keywords that decrease indent
    dedent_keywords = ['סוף', 'אחרת']
    
    for line in lines:
        stripped = line.strip()
        
        # Check for dedent keywords before processing this line
        if any(stripped.startswith(keyword) for keyword in dedent_keywords):
            indent_level -= 1 if indent_level > 0 else 0
        
        # Format the line with proper RTL-friendly indentation
        # In RTL languages, indentation is typically added to the right side
        # We'll use non-breaking spaces for indentation to preserve alignment
        if stripped and not stripped.startswith('#'):  # Skip empty lines and comments
            # Calculate right-side padding for RTL display
            padding = '\u00A0' * (4 * indent_level)  # non-breaking space
            formatted_line = padding + line.strip()
        else:
            formatted_line = line  # Keep comments and empty lines as is
        
        formatted_lines.append(formatted_line)
        
        # Check for indent keywords after processing this line
        if any(stripped.startswith(keyword) for keyword in indent_keywords):
            indent_level += 1
    
    return '\n'.join(formatted_lines)

def add_rtl_marks(code):
    """Add RTL marks to improve display of Hebrew text."""
    # Add RTL mark at the beginning of each Hebrew text section
    rtl_mark = '\u200F'  # Right-to-Left Mark
    
    def add_rtl_to_line(line):
        # Don't add RTL marks to empty lines or comments
        if not line.strip() or line.strip().startswith('#'):
            return line
        
        # Add RTL mark if line contains Hebrew characters
        if re.search('[א-ת]', line):
            return rtl_mark + line
        return line
    
    lines = code.split('\n')
    rtl_lines = [add_rtl_to_line(line) for line in lines]
    return '\n'.join(rtl_lines)

if __name__ == "__main__":
    # Test the formatter
    test_code = """# תכנית לדוגמה
קבע א = 10
קבע ב = 5

אם א > ב
    הדפס "א גדול מב"
    קבע ג = א * 2
אחרת
    הדפס "ב גדול או שווה לא"
סוף

הדפס ג
"""
    
    formatted = format_aron_code(test_code)
    with_rtl_marks = add_rtl_marks(formatted)
    print(with_rtl_marks)
