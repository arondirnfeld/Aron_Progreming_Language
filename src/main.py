# src/main.py
import sys
import os
from lexer import tokenize
from parser import parse
from interpreter import interpret

# Try to import the RTL console setup if on Windows
try:
    from set_console_rtl import set_console_rtl_mode
    set_console_rtl_mode()
except ImportError:
    pass  # Not critical if it fails

# Import the RTL formatter
try:
    from rtl_formatter import format_aron_code, add_rtl_marks
except ImportError:
    # Fallback if the formatter is not available
    def format_aron_code(code): return code
    def add_rtl_marks(code): return code

def run_aron_file(filepath, debug=False):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Format code for better RTL display
        formatted_code = format_aron_code(code)
        
        # Add RTL mark to ensure proper direction
        print("\u200F--- Executing Aron file: {filepath} ---")
        
        # Optional: Display the formatted code
        if debug:
            print("\u200F--- Formatted Source Code ---")
            print(add_rtl_marks(formatted_code))
            print("\u200F---------------------------")
        
        try:
            tokens = tokenize(code)  # Still tokenize the original code
            
            if debug:
                print("\u200FDEBUG: Tokens generated:")
                for token in tokens:
                    print(f"\u200F  {token}")
            
            try:
                ast_nodes = parse(tokens)
                
                if debug:
                    print("DEBUG: AST nodes:")
                    for node in ast_nodes:
                        print(f"  {node}")
                
                try:
                    interpret(ast_nodes)
                except RuntimeError as e:
                    print(f"Runtime Error: {e}")
                    
            except SyntaxError as e:
                print(f"Syntax Error: {e}")
                
        except RuntimeError as e:
            print(f"Lexical Error: {e}")
            
        print(f"--- Finished execution ---")

    except FileNotFoundError:
        print(f"Error: File not found '{filepath}'")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def print_usage():
    print("שפת אהרן - Aron Programming Language")
    print("\nUsage:")
    print("  python main.py <filepath.aron> [options]")
    print("\nOptions:")
    print("  --debug    Show debugging information (tokens and AST)")
    print("  --help     Show this help message")
    print("\nExamples:")
    print("  python main.py examples/hello.aron")
    print("  python main.py examples/final.aron --debug")
    print("\nFeatures Implemented:")
    print("  * Comments with #")
    print("  * Variables with קבע")
    print("  * Print statements with הדפס")
    print("  * Arithmetic operations (+, -, *, /)")
    print("  * Parenthesized expressions")
    print("  * Boolean values (אמת/שקר)")
    print("  * Comparison operators (==, !=, <, >, <=, >=)")
    print("  * If-else statements (אם, אחרת, סוף)")
    print("  * String operations (concatenation)")
    print("\nFuture Development:")
    print("  * Functions")
    print("  * Data structures (arrays, lists)")
    print("  * Loops (while, for)")
    print("  * Importing files and libraries")
    print("  * Dedicated IDE")

def list_examples():
    examples_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'examples')
    if os.path.exists(examples_dir):
        examples = [f for f in os.listdir(examples_dir) if f.endswith('.aron')]
        if examples:
            print("\nAvailable examples:")
            for example in examples:
                print(f"  python main.py examples/{example}")

if __name__ == "__main__":
    if len(sys.argv) < 2 or "--help" in sys.argv:
        print_usage()
        list_examples()
        sys.exit(0 if "--help" in sys.argv else 1)
    
    filepath = sys.argv[1]
    debug_mode = "--debug" in sys.argv
    
    run_aron_file(filepath, debug_mode)
