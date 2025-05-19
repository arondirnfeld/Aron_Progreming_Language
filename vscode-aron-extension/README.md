# Aron Language Support for VS Code

This extension provides language support for the Aron (אהרן) programming language, including syntax highlighting, code completion, and the ability to run Aron files directly from VS Code.

## Features

- Syntax highlighting for Aron source files (.aron)
- Code completion for Aron keywords (הדפס, קבע, אם, אחרת, סוף, אמת, שקר)
- Hover information for Aron keywords
- Run Aron files directly from the editor context menu
- Language configuration (bracket matching, comment toggling)
- Right-to-Left (RTL) support for Hebrew language

## RTL Support

As Aron is a Hebrew-based programming language, this extension automatically enables Right-to-Left (RTL) mode in the editor when an Aron file is opened. You can toggle between RTL and LTR modes by:

- Right-clicking on the editor and selecting "Toggle RTL mode for Aron" 
- Using the Command Palette (Ctrl+Shift+P) and typing "Toggle RTL mode for Aron"

### RTL Formatting

To improve readability of Aron code in RTL mode, you can format your code with proper RTL indentation:

- Right-click on the editor and select "Format Aron File for RTL"
- Using the Command Palette (Ctrl+Shift+P) and typing "Format Aron File for RTL"

This will format the code with proper indentation for RTL display, making it more readable in Hebrew.

## How to Use

1. Install the extension
2. Open an Aron file (with `.aron` extension)
3. Use the right-click context menu and select "Run Aron File" to execute the file

## Run Command

You can run an Aron file by:
- Right-clicking on the editor and selecting "Run Aron File"
- Using the Command Palette (Ctrl+Shift+P) and typing "Run Aron File"

## Keyboard Shortcut

You can also set up a keyboard shortcut by adding the following to your keyboard shortcuts settings:

```json
{
  "key": "ctrl+f5",
  "command": "aron.run",
  "when": "editorLangId == aron"
}
```

## Aron Language Features

The Aron language supports:

- Variables (using קבע)
- Print statements (using הדפס)
- Arithmetic operations (+, -, *, /)
- Parenthesized expressions
- Boolean values (אמת/שקר)
- Comparison operators (==, !=, <, >, <=, >=)
- If-else statements (אם, אחרת, סוף)
- Comments (using #)
- String operations (concatenation)

## Examples

```
# משתנים ופעולות חשבוניות
קבע א = 10
קבע ב = 5
קבע סכום = א + ב
הדפס סכום

# תנאים
אם א > ב
    הדפס "א גדול מב"
אחרת
    הדפס "א קטן או שווה לב"
סוף

# מחרוזות
קבע שם = "אהרן"
קבע שם_מלא = שם + " הכהן"
הדפס שם_מלא
```

## Requirements

This extension requires a properly installed Aron language interpreter (main.py) located in the src directory of the Aron language project.

## Extension Settings

This extension doesn't add any VS Code settings yet.

## Known Issues

- Hebrew characters may not display correctly in some terminal environments
- This is an early version with basic functionality

## Release Notes

### 0.0.1

Initial release of Aron language support including:
- Basic syntax highlighting
- Code completion for keywords
- Run command integration
