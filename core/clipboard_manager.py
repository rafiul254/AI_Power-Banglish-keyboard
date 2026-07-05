"""
clipboard_manager.py — Clipboard read/write utilities
"""
import pyperclip
import time


def get_text() -> str:
    """Get current clipboard content. Returns empty string on failure."""
    try:
        content = pyperclip.paste()
        return content if content else ""
    except Exception as e:
        print(f"[Clipboard] Read error: {e}")
        return ""


def set_text(text: str) -> bool:
    """Set clipboard content. Returns True on success."""
    try:
        pyperclip.copy(text)
        time.sleep(0.05)  # Let clipboard settle
        return True
    except Exception as e:
        print(f"[Clipboard] Write error: {e}")
        return False


def save_and_set(new_text: str) -> str:
    """
    Save current clipboard, then set new text.

    Returns:
        The original clipboard content (so caller can restore it later).
    """
    original = get_text()
    set_text(new_text)
    return original
