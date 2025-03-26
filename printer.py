import os
import win32print
import win32api



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
