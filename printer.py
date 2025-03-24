import os
import win32print
import win32api

def print_file(file_path):
    try:
        printer_name = win32print.GetDefaultPrinter()
        print(f"🖨️ Printing using {printer_name}...")

        # Print using the default application
        win32api.ShellExecute(0, "print", file_path, None, ".", 0)
        print("✅ Print job sent successfully!")
    except Exception as e:
        print(f"❌ Error while printing: {e}")
