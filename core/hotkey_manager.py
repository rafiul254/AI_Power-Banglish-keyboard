"""
hotkey_manager.py — Global hotkey listener + conversion trigger

Flow when hotkey pressed:
  1. Select all text in the focused field  (Ctrl+A)
  2. Copy it to clipboard                  (Ctrl+C)
  3. Send text → Claude API
  4. Paste converted text back             (Ctrl+V)
  5. Restore original clipboard content

NOTE: On Windows, run as normal user. On Linux, requires root (sudo).
"""
import keyboard
import pyperclip
import time
import threading
from typing import Callable, Optional

from core.ai_converter import convert_banglish
from config.settings import load_config


class HotkeyManager:
    """
    Registers and manages global keyboard shortcuts.

    Usage:
        manager = HotkeyManager(status_callback=my_fn)
        thread = threading.Thread(target=manager.start, daemon=True)
        thread.start()
    """

    def __init__(self, status_callback: Optional[Callable[[str], None]] = None):
        self.status_callback = status_callback
        self._registered = False
        self._processing = False  # Prevent overlapping conversions

    # ─────────────────────────────────────────────────────────────
    # Internal helpers
    # ─────────────────────────────────────────────────────────────

    def _notify(self, msg: str):
        print(f"[HotkeyManager] {msg}")
        if self.status_callback:
            self.status_callback(msg)

    def _grab_field_text(self) -> tuple[str, str]:
        """
        Select all text in the current field and copy it.

        Returns:
            (copied_text, original_clipboard)
        """
        original_clipboard = pyperclip.paste()   # backup clipboard
        pyperclip.copy("")                        # clear so we detect success
        time.sleep(0.05)

        keyboard.press_and_release("ctrl+a")      # select all
        time.sleep(0.12)
        keyboard.press_and_release("ctrl+c")      # copy
        time.sleep(0.25)                          # wait for OS clipboard

        copied = pyperclip.paste()
        return copied, original_clipboard

    def _paste_text(self, text: str):
        """Put text in clipboard and paste into the focused field."""
        pyperclip.copy(text)
        time.sleep(0.1)
        keyboard.press_and_release("ctrl+v")
        time.sleep(0.1)

    # ─────────────────────────────────────────────────────────────
    # Core conversion flow
    # ─────────────────────────────────────────────────────────────

    def _run_conversion(self, target: str):
        """
        Full conversion pipeline. Runs in a background thread so
        the hotkey listener is never blocked.

        Args:
            target: "bangla" or "english"
        """
        if self._processing:
            self._notify("⏳ Still processing... please wait")
            return

        self._processing = True
        label = "বাংলা" if target == "bangla" else "English"

        try:
            self._notify(f"⏳ Converting to {label}...")

            # Step 1 — Grab text
            text, original_clip = self._grab_field_text()

            if not text.strip():
                self._notify("⚠️ No text found! Type Banglish first.")
                pyperclip.copy(original_clip)
                return

            # Step 2 — Call Claude API
            result = convert_banglish(text, target)

            if result.startswith("❌"):
                self._notify(result)
                pyperclip.copy(original_clip)
                return

            # Step 3 — Replace text in field
            self._paste_text(result)

            # Step 4 — Restore original clipboard
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

    # ─────────────────────────────────────────────────────────────
    # Public API
    # ─────────────────────────────────────────────────────────────

    def register(self):
        """Read config and register hotkeys."""
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
        """Remove all registered hotkeys."""
        keyboard.unhook_all_hotkeys()
        self._registered = False
        self._notify("🔴 Hotkeys cleared")

    def reload(self):
        """Reload hotkeys (call after user changes config)."""
        self.unregister()
        time.sleep(0.1)
        self.register()

    def start(self):
        """Register hotkeys and block until program exits."""
        self.register()
        keyboard.wait()   # Blocking — keeps the thread alive

    def stop(self):
        """Stop listening."""
        self.unregister()
