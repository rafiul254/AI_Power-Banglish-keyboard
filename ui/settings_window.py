"""
settings_window.py — Dark-themed Tkinter settings GUI.
"""
import tkinter as tk
from tkinter import ttk
from config.settings import load_config, save_config

BG      = "#1e1e2e"
SURFACE = "#313244"
ACCENT  = "#7c3aed"
TEXT    = "#cdd6f4"
SUBTEXT = "#6c7086"
GREEN   = "#a6e3a1"
RED     = "#f38ba8"
BORDER  = "#45475a"


class SettingsWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Banglish Keyboard — Settings")
        self.root.geometry("520x500")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.root.eval("tk::PlaceWindow . center")

        self.config = load_config()
        self._vars: dict[str, tk.StringVar] = {}

        self._build_ui()

    def _lbl(self, parent, text, fg=TEXT, size=10, bold=False):
        font = ("Segoe UI", size, "bold") if bold else ("Segoe UI", size)
        return tk.Label(parent, text=text, bg=BG, fg=fg, font=font)

    def _entry(self, parent, var, show=None):
        return tk.Entry(
            parent,
            textvariable=var,
            show=show,
            bg=SURFACE,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Segoe UI", 10),
            width=36,
            highlightthickness=1,
            highlightcolor=ACCENT,
            highlightbackground=BORDER,
        )

    def _build_ui(self):
        tk.Frame(self.root, bg=ACCENT, height=3).pack(fill="x")

        self._lbl(self.root, "🤖  AI Banglish Keyboard", fg=ACCENT, size=17, bold=True).pack(pady=(22, 3))
        self._lbl(self.root, "Configuration & Settings", fg=SUBTEXT, size=10).pack(pady=(0, 22))

        form = tk.Frame(self.root, bg=BG)
        form.pack(padx=44, fill="x")

        rows = [
            ("Groq API Key",      "api_key",           "*"),
            ("Hotkey → বাংলা",   "hotkey_to_bangla",   None),
            ("Hotkey → English",  "hotkey_to_english",  None),
        ]

        for i, (label, key, show) in enumerate(rows):
            self._lbl(form, label + ":").grid(row=i, column=0, sticky="w", pady=10)
            var = tk.StringVar(value=self.config.get(key, ""))
            self._vars[key] = var
            self._entry(form, var, show=show).grid(row=i, column=1, pady=10, padx=(14, 0))

        # Model selector
        self._lbl(form, "AI Model:").grid(row=3, column=0, sticky="w", pady=10)

        model_var = tk.StringVar(value=self.config.get("model", "llama-3.3-70b-versatile"))
        self._vars["model"] = model_var

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.TCombobox",
            fieldbackground=SURFACE,
            background=SURFACE,
            foreground=TEXT,
            selectbackground=ACCENT,
        )

        ttk.Combobox(
            form,
            textvariable=model_var,
            values=["llama-3.3-70b-versatile", "llama3-8b-8192", "gemma2-9b-it"],
            width=35,
            state="readonly",
            style="Custom.TCombobox",
        ).grid(row=3, column=1, pady=10, padx=(14, 0))

        # Save button
        tk.Button(
            self.root,
            text="  💾   Save Settings  ",
            command=self._save,
            bg=ACCENT,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=18, pady=10,
            cursor="hand2",
            activebackground="#6d28d9",
            activeforeground="white",
        ).pack(pady=22)

        # Status message
        self.status_var = tk.StringVar(value="")
        self.status_lbl = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg=BG, fg=GREEN,
            font=("Segoe UI", 10),
        )
        self.status_lbl.pack()

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=40, pady=(20, 10))

        help_lines = [
            "Get your FREE Groq API key →  console.groq.com",
            "Hotkey examples:  ctrl+shift+b   |   alt+b   |   f9",
        ]
        for line in help_lines:
            self._lbl(self.root, line, fg=SUBTEXT, size=9).pack(pady=1)

    def _save(self):
        new_config = {key: var.get().strip() for key, var in self._vars.items()}

        if not new_config.get("api_key"):
            self.status_var.set("⚠️  API Key cannot be empty!")
            self.status_lbl.config(fg=RED)
            return

        if save_config(new_config):
            self.config = new_config
            self.status_var.set("✅  Saved! Restart the app to apply hotkey changes.")
            self.status_lbl.config(fg=GREEN)
        else:
            self.status_var.set("❌  Could not save settings.")
            self.status_lbl.config(fg=RED)

    def show(self):
        self.root.mainloop()
