# set_console_rtl.py
# Utility script to configure Windows console for better RTL support

import ctypes
import sys
import os

def set_console_rtl_mode():
    """Set the console to support RTL text properly."""
    if sys.platform != 'win32':
        print("This script is intended for Windows only.")
        return
    
    try:
        # Get console output handle
        STD_OUTPUT_HANDLE = -11
        console_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        
        # Current mode flags
        mode = ctypes.c_uint32()
        ctypes.windll.kernel32.GetConsoleMode(console_handle, ctypes.byref(mode))
        
        # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        # This allows for ANSI escape sequences
        ctypes.windll.kernel32.SetConsoleMode(console_handle, mode.value | 0x0004)
        
        # Set the console output codepage to UTF-8
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)  # 65001 is the code page for UTF-8
        
        print("Console configured for RTL text support.")
        print("You may need to change the console font to one that supports Hebrew characters.")
        print("Recommended fonts: Courier New, Consolas, or any font that supports Hebrew.")
    except Exception as e:
        print(f"Error configuring console: {e}")

if __name__ == "__main__":
    set_console_rtl_mode()
