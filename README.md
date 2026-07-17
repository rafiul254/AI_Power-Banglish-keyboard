<div align="center">

# 🤖 AI Banglish Keyboard & Converter

**Convert Banglish → বাংলা or English instantly.**
*One hotkey on desktop. One tap on Android.*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Kotlin](https://img.shields.io/badge/Kotlin-Android-7c3aed?style=flat&logo=kotlin&logoColor=white)](https://kotlinlang.org)
[![Groq](https://img.shields.io/badge/Powered%20by-Groq%20AI-orange?style=flat)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Android-blue?style=flat)]()

*Built by [Rafiul Islam](https://github.com/rafiul254) — IoT & Robotics Engineer, UFTB*

</div>

---

## 📌 What Is This?

Bangladeshis type in **Banglish** everywhere — Bengali written in English/Roman script, mixed with actual English words.

> *"ami aj office theke fire khub tired, ektu help lagbe"*

This project gives you **two tools** that detect that text and convert it instantly using Groq AI (free).

---

## ✨ Features

- 🔥 Works in **any app** — WhatsApp Web, Notepad, Chrome, VS Code, anywhere
- ⚡ Powered by **Groq AI** — free tier, no credit card needed
- 🎯 Understands informal Banglish, slang, and social media language
- 🖥️ **Desktop:** Runs silently in system tray, always ready
- 📱 **Android:** Standalone app with copy & share support
- ⌨️ Fully customizable hotkeys (Desktop)
- 🌙 Dark themed UI

---

## 🖥️ Desktop Version (Windows / Linux)

Sits in your **system tray** and converts text in any app with a hotkey.

| Hotkey | Result |
|---|---|
| `Ctrl+Shift+B` | Converts selected text to **বাংলা** Unicode |
| `Ctrl+Shift+E` | Converts selected text to clean **English** |

### Quick Start

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

On first launch, a **Settings window** opens automatically.
Enter your **Groq API key** and click Save.

### Build EXE (Windows — run without Python)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="AI-Keyboard" main.py
```

EXE will be in `dist/AI-Keyboard.exe`

**Auto-start on Windows boot:**
Windows + R → shell:startup → paste shortcut of AI-Keyboard.exe here

---

## 📱 Android Version

A standalone **converter app** — open it, type Banglish, tap a button, done.
No keyboard replacement. Works alongside Gboard or any other keyboard.

### Features

| Button | Action |
|---|---|
| **AI → বাংলা** | Converts Banglish to proper Bengali Unicode |
| **AI → English** | Converts to clean grammatical English |
| **Copy** | One-tap copy to clipboard |
| **Share** | Share directly to WhatsApp, Messenger, etc |
| **Settings** | Save your Groq API key |

### Install

👉 [Download APK](../../releases) — install directly on your Android phone (no Play Store needed)

### Build from Source

Open android-app/ folder in IntelliJ IDEA
Sync Gradle (File → Sync Project with Gradle Files)
Connect phone via USB (enable USB Debugging)
Run ▶


---

## 🏗️ Project Structure
AI_power-banglish-keyboard/
│
├── desktop/                        ← Python desktop app
│   ├── main.py                     ← Entry point
│   ├── requirements.txt
│   ├── config/
│   │   └── settings.py            ← Config manager (API key, hotkeys)
│   ├── core/
│   │   ├── ai_converter.py        ← Groq API integration
│   │   ├── hotkey_manager.py      ← Global hotkey listener
│   │   └── clipboard_manager.py
│   └── ui/
│       ├── tray_icon.py           ← System tray icon
│       └── settings_window.py     ← Tkinter settings GUI
│
└── android-app/                    ← Android Kotlin app
└── app/src/main/
├── kotlin/com/rafiul/
│   ├── MainActivity.kt    ← Main converter screen
│   ├── SettingsActivity.kt← API key settings
│   └── AIConverter.kt     ← Groq REST API client
└── res/
├── layout/
│   ├── activity_main.xml
│   └── activity_settings.xml
└── values/themes.xml

---

## ⚙️ How It Works
User types Banglish in any text field
↓
Press hotkey (Desktop) or tap button (Android)
↓
Text sent to Groq AI with prompt:
"Convert Banglish to বাংলা / English.
Preserve tone and emotion exactly."
↓
AI returns converted text instantly
↓
Original text replaced / shown in output ✅

---

## 🆓 Groq Free Tier

| Limit | Value |
|---|---|
| Requests / minute | 30 |
| Requests / day | 14,400 |
| Cost | **$0 forever** |

Get your free key at **[console.groq.com](https://console.groq.com)**

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Desktop Language | Python 3.10+ |
| AI Engine | Groq API — `llama-3.3-70b-versatile` |
| Hotkey Listener | `keyboard` library |
| System Tray | `pystray` + `Pillow` |
| Desktop GUI | `tkinter` |
| Desktop Packaging | `PyInstaller` |
| Android Language | Kotlin |
| Android HTTP | OkHttp |
| Android Async | Coroutines |
| Distribution | GitHub Releases |

---

## 📦 Download & Distribution

| Platform | Method | Link |
|---|---|---|
| Windows EXE | GitHub Releases | [Download](../../releases) |
| Android APK | GitHub Releases | [Download](../../releases) |
| Android APK | F-Droid (coming soon) | — |
| Source Code | GitHub | This repo |

---

## 🗺️ Roadmap

- [x] Desktop Python app with system tray
- [x] Global hotkey conversion (Ctrl+Shift+B / E)
- [x] Android standalone converter app
- [x] Copy & Share support
- [ ] History of past conversions
- [ ] Auto-detect Banglish vs pure English
- [ ] Offline fallback (rule-based)
- [ ] Flutter cross-platform version (iOS + Android)
- [ ] Number row & symbols on mobile keyboard

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

1. Fork the repo
2. Create your branch (`git checkout -b feature/amazing-feature`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">

*"Built because typing বাংলা shouldn't require switching keyboards."*

⭐ **Star this repo if it helped you!**

[GitHub](https://github.com/rafiul254) · [LinkedIn](https://www.linkedin.com/in/rafiul-islam-25sep92004) · [YouTube](https://youtube.com/@pintocloud?si=bMQQySdz6Sz6r4z2) 

</div>
