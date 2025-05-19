# src/main.py
import sys
import os
from lexer import tokenize
from parser import parse
from interpreter import interpret

def run_aron_file(filepath, debug=False):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        print(f"--- Executing Aron file: {filepath} ---")
        
        try:
            tokens = tokenize(code)
            
            if debug:
                print("DEBUG: Tokens generated:")
                for token in tokens:
                    print(f"  {token}")
            
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
