import os
import win32print
import win32api

def print_file(file_path):
    """
    Print the given file using the default printer.

    Args:
        file_path (str): Path to the file to print.
    """
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    try:
        print("🖨️ Sending file to the printer...")
        win32api.ShellExecute(0, "print", file_path, None, ".", 0)
        print(f"✅ Printing started: {file_path}")
    except Exception as e:
        print(f"❌ Error while printing: {e}")

def get_default_printer():
    """
    Get the current default printer.

    Returns:
        str: Name of the default printer or None if unavailable.
    """
    try:
        printer_name = win32print.GetDefaultPrinter()
        print(f"🖨️ Default Printer: {printer_name}")
        return printer_name
    except Exception as e:
        print(f"❌ Error fetching default printer: {e}")
        return None

def test_print():
    """
    Perform a test print using a sample text file.
    """
    try:
        sample_text = "C:\\Windows\\System32\\notepad.exe"  # Using Notepad for test print
        print_file(sample_text)
    except Exception as e:
        print(f"❌ Test print failed: {e}")
