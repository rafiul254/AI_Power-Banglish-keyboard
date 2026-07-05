import sys
import os
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import load_config
from core.hotkey_manager import HotkeyManager
from ui.tray_icon import TrayIcon
from ui.settings_window import SettingsWindow


class AIKeyboardApp:
    """
    Top-level application class. Wires together:
      • HotkeyManager  (background daemon thread)
      • TrayIcon       (main thread — blocking)
      • SettingsWindow (spawned on demand)
    """

    def __init__(self):
        self.tray:           TrayIcon      = None
        self.hotkey_manager: HotkeyManager = None


    def _on_status(self, message: str):
        """Bubble status updates from HotkeyManager to the tray icon."""
        if self.tray:
            self.tray.update_status(message)

    def _open_settings(self):
        """Show settings window (runs in its own thread to stay non-blocking)."""
        win = SettingsWindow()
        win.show()

    def _reload_hotkeys(self):
        if self.hotkey_manager:
            self.hotkey_manager.reload()

    def _quit(self):
        print("\n[App] Shutting down — goodbye! 👋")
        if self.hotkey_manager:
            self.hotkey_manager.stop()
        sys.exit(0)


    def _first_run_check(self):
        """If no API key is saved, open Settings before anything else."""
        cfg = load_config()
        if not cfg.get("api_key", "").strip():
            print("[App] First run — opening Settings to collect API key...")
            self._open_settings()


    def run(self):
        print("=" * 55)
        print("  🤖  AI Banglish Keyboard — Starting...")
        print("=" * 55)

        self._first_run_check()

        self.hotkey_manager = HotkeyManager(status_callback=self._on_status)

        self.tray = TrayIcon(
            on_settings=self._open_settings,
            on_reload=self._reload_hotkeys,
            on_quit=self._quit,
        )

        t = threading.Thread(
            target=self.hotkey_manager.start,
            daemon=True,
            name="HotkeyListenerThread",
        )
        t.start()

        cfg = load_config()
        print(f"\n  Hotkeys:")
        print(f"    {cfg.get('hotkey_to_bangla', 'ctrl+shift+b'):<20}→  বাংলা")
        print(f"    {cfg.get('hotkey_to_english', 'ctrl+shift+e'):<20}→  English")
        print("\n  Running in system tray. Right-click icon for menu.")
        print("  Focus any text field and press a hotkey to convert.\n")

        self.tray.run()


if __name__ == "__main__":
    app = AIKeyboardApp()
    app.run()
