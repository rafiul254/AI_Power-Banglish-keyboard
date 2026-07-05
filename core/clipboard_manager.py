import pyperclip
import time


def get_text() -> str:
    try:
        content = pyperclip.paste()
        return content if content else ""
    except Exception as e:
        print(f"[Clipboard] Read error: {e}")
        return ""


def set_text(text: str) -> bool:

    try:
        pyperclip.copy(text)
        time.sleep(0.05)  
        return True
    except Exception as e:
        print(f"[Clipboard] Write error: {e}")
        return False


def save_and_set(new_text: str) -> str:

    original = get_text()
    set_text(new_text)
    return original
