import keyboard
import pyperclip
import time
import threading
from typing import Callable, Optional

from core.ai_converter import convert_banglish
from config.settings import load_config


class HotkeyManager:


    def __init__(self, status_callback: Optional[Callable[[str], None]] = None):
        self.status_callback = status_callback
        self._registered = False
        self._processing = False  


    def _notify(self, msg: str):
        print(f"[HotkeyManager] {msg}")
        if self.status_callback:
            self.status_callback(msg)

    def _grab_field_text(self) -> tuple[str, str]:
     
        original_clipboard = pyperclip.paste()   
        pyperclip.copy("")                       
        time.sleep(0.05)

        keyboard.press_and_release("ctrl+a")     
        time.sleep(0.12)
        keyboard.press_and_release("ctrl+c")    
        time.sleep(0.25)                          

        copied = pyperclip.paste()
        return copied, original_clipboard

    def _paste_text(self, text: str):
       
        pyperclip.copy(text)
        time.sleep(0.1)
        keyboard.press_and_release("ctrl+v")
        time.sleep(0.1)


    def _run_conversion(self, target: str):
 
        if self._processing:
            self._notify("⏳ Still processing... please wait")
            return

        self._processing = True
        label = "বাংলা" if target == "bangla" else "English"

        try:
            self._notify(f"⏳ Converting to {label}...")

            text, original_clip = self._grab_field_text()

            if not text.strip():
                self._notify("⚠️ No text found! Type Banglish first.")
                pyperclip.copy(original_clip)
                return

            result = convert_banglish(text, target)

            if result.startswith("❌"):
                self._notify(result)
                pyperclip.copy(original_clip)
                return

            self._paste_text(result)

        
            time.sleep(0.2)
            pyperclip.copy(original_clip)

            self._notify(f"✅ Converted to {label}!")

        except Exception as e:
            self._notify(f"❌ Unexpected error: {str(e)[:70]}")
        finally:
            self._processing = False

    def _on_bangla(self):
        threading.Thread(
            target=self._run_conversion, args=("bangla",), daemon=True
        ).start()

    def _on_english(self):
        threading.Thread(
            target=self._run_conversion, args=("english",), daemon=True
        ).start()



    def register(self):
      
        config = load_config()
        hk_bn = config.get("hotkey_to_bangla", "ctrl+shift+b")
        hk_en = config.get("hotkey_to_english", "ctrl+shift+e")

        try:
            keyboard.add_hotkey(hk_bn, self._on_bangla, suppress=True)
            keyboard.add_hotkey(hk_en, self._on_english, suppress=True)
            self._registered = True
            self._notify(f"✅ Hotkeys active — {hk_bn} (বাংলা) | {hk_en} (English)")
        except Exception as e:
            self._notify(f"❌ Hotkey registration failed: {e}")

    def unregister(self):
      
        keyboard.unhook_all_hotkeys()
        self._registered = False
        self._notify("🔴 Hotkeys cleared")

    def reload(self):
     
        self.unregister()
        time.sleep(0.1)
        self.register()

    def start(self):

        self.register()
        keyboard.wait()  

    def stop(self):
        self.unregister()
