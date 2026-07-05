"""
tray_icon.py — System tray icon with right-click context menu.
Icon is generated dynamically (no external .ico file needed).
"""
import pystray
from PIL import Image, ImageDraw
import threading
from typing import Callable, Optional


# ── Icon generator ────────────────────────────────────────────────────────────

def _make_icon(color: str = "#7c3aed") -> Image.Image:
    """
    Draw a 64×64 purple circle with a white 'AI' glyph.
    Pure PIL — no fonts required.
    """
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Background circle
    d.ellipse([2, 2, 62, 62], fill=color)

    # 'A' glyph (simple pixel-art style)
    d.polygon([(14, 46), (10, 46), (20, 18), (24, 18)], fill="white")
    d.polygon([(26, 46), (22, 46), (20, 18), (24, 18)], fill="white")
    d.rectangle([13, 34, 25, 37], fill="white")

    # 'I' glyph
    d.rectangle([32, 18, 36, 46], fill="white")
    d.rectangle([29, 18, 39, 22], fill="white")
    d.rectangle([29, 42, 39, 46], fill="white")

    return img


# ── TrayIcon class ────────────────────────────────────────────────────────────

class TrayIcon:
    """
    Wraps pystray.Icon with a clean API.

    Constructor args (all optional callables):
        on_settings — called when user clicks Settings
        on_reload   — called when user clicks Reload Hotkeys
        on_quit     — called when user clicks Quit
    """

    def __init__(
        self,
        on_settings: Optional[Callable] = None,
        on_reload:   Optional[Callable] = None,
        on_quit:     Optional[Callable] = None,
    ):
        self.on_settings = on_settings
        self.on_reload   = on_reload
        self.on_quit     = on_quit

        self._icon: Optional[pystray.Icon] = None
        self._status = "Ready"

    # ── Status updates ────────────────────────────────────────────

    def update_status(self, message: str):
        """Update the tray tooltip text."""
        self._status = message
        if self._icon:
            self._icon.title = f"AI Keyboard — {message}"

    # ── Menu callbacks ────────────────────────────────────────────

    def _open_settings(self, icon, item):
        if self.on_settings:
            threading.Thread(target=self.on_settings, daemon=True).start()

    def _reload_hotkeys(self, icon, item):
        if self.on_reload:
            threading.Thread(target=self.on_reload, daemon=True).start()

    def _quit_app(self, icon, item):
        icon.stop()
        if self.on_quit:
            self.on_quit()

    def _status_text(self, item) -> str:
        return f"Status: {self._status}"

    # ── Public: run ───────────────────────────────────────────────

    def run(self):
        """Start the tray icon. Blocking — call from main thread."""
        menu = pystray.Menu(
            pystray.MenuItem(self._status_text, None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Ctrl+Shift+B  →  বাংলা",  None, enabled=False),
            pystray.MenuItem("Ctrl+Shift+E  →  English", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("⚙️  Settings",       self._open_settings),
            pystray.MenuItem("🔄  Reload Hotkeys", self._reload_hotkeys),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("❌  Quit",            self._quit_app),
        )

        self._icon = pystray.Icon(
            name="AI Banglish Keyboard",
            icon=_make_icon(),
            title="AI Banglish Keyboard — Ready",
            menu=menu,
        )
        self._icon.run()
