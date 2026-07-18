<div align="center">

# 🤖 AI Banglish Keyboard

**Convert Banglish → বাংলা or English instantly with a hotkey.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Groq](https://img.shields.io/badge/Powered%20by-Groq%20AI-orange?style=flat)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue?style=flat)]()

*Built by [Rafiul Islam](https://github.com/rafiul254)*

</div>

---

## 📌 What Is This?

Bangladeshis type in **Banglish** everywhere — Bengali words written in 
English script, mixed with actual English.

> *"ami aj office theke fire khub tired, ektu help lagbe"*

This tool sits in your **system tray** and converts that text instantly 
using Groq AI (free).

| Hotkey | Result |
|---|---|
| `Ctrl+Shift+B` | Converts to **বাংলা** Unicode |
| `Ctrl+Shift+E` | Converts to clean **English** |

---

## ✨ Features

- 🔥 Works in **any app** — WhatsApp Web, Notepad, Chrome, VS Code, anywhere
- ⚡ Powered by **Groq AI** (free tier, no credit card needed)
- 🎯 Understands informal Banglish, slang, and social media language
- 🖥️ Runs silently in the **system tray** — always ready
- ⌨️ Fully **customizable hotkeys**
- 🌙 Dark themed settings UI

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Free Groq API key from [console.groq.com](https://console.groq.com)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/rafiul254/ai-banglish-keyboard.git
cd ai-banglish-keyboard/desktop

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python main.py
```

On first launch, a Settings window opens automatically.
Enter your Groq API key and click **Save**.

---

## Project Structure

```
ai-banglish-keyboard/
desktop/
├── main.py                 ← Entry point
├── requirements.txt
├── config/
│   └── settings.py        ← Config manager (API key, hotkeys)
├── core/
│   ├── ai_converter.py    ← Groq API integration
│   ├── hotkey_manager.py  ← Global hotkey listener
│   └── clipboard_manager.py
└── ui/
├── tray_icon.py       ← System tray icon
└── settings_window.py ← Tkinter settings GUI

---

## 🖥️ Build EXE (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="AI-Keyboard" main.py
```

Executable will be in `dist/AI-Keyboard.exe`.

**Auto-start on Windows boot:**
Windows + R → shell:startup → paste shortcut of AI-Keyboard.exe

---

## ⚙️ How It Works
You type Banglish in any text field
↓
Press Ctrl+Shift+B
↓
App grabs text → sends to Groq AI
↓
AI converts to বাংলা / English
↓
Original text replaced instantly ✅

---

## 🆓 Groq Free Tier Limits

| Limit | Value |
|---|---|
| Requests / minute | 30 |
| Requests / day | 14,400 |
| Cost | **$0 forever** |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| AI Engine | Groq API (llama-3.3-70b-versatile) |
| Hotkeys | `keyboard` library |
| Tray Icon | `pystray` + `Pillow` |
| GUI | `tkinter` |
| Packaging | `PyInstaller` |

---

## Roadmap

- [x] Desktop Python app with hotkeys
- [x] Android custom IME keyboard
- [ ] Number row on keyboard
- [ ] Symbol layer (long-press keys)
- [ ] Auto-detect language mode
- [ ] Offline fallback (rule-based)
- [ ] Dark/light theme toggle
- [ ] Voice input support

---

## 📄 License

MIT License — free to use, modify, distribute.

---

<div align="center">

*"Built because typing বাংলা shouldn't require switching keyboards."*

⭐ Star this repo if it helped you!

</div>

