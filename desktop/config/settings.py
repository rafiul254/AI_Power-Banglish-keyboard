"""
settings.py — App configuration manager
Saves/loads config from user's home directory as JSON.
"""
import json
import os

# Config stored in user home — survives app updates
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".ai_keyboard_config.json")

DEFAULT_CONFIG = {
    "api_key": "",
    "model": "llama-3.3-70b-versatile",
    "hotkey_to_bangla": "ctrl+shift+b",
    "hotkey_to_english": "ctrl+shift+e",
}


def load_config() -> dict:
    """Load config from disk, merging with defaults for any missing keys."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                # Merge: saved values override defaults
                return {**DEFAULT_CONFIG, **saved}
        except (json.JSONDecodeError, IOError):
            pass  # Fall through to return defaults
    return DEFAULT_CONFIG.copy()


def save_config(config: dict) -> bool:
    """Save config dict to disk. Returns True on success."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"[Config] Failed to save: {e}")
        return False


def get(key: str, default=None):
    """Shortcut to get a single config value."""
    return load_config().get(key, default)
