# 🚀 App Opener X (Cyberpunk Edition)

A smart, lightweight application manager built with Python. It features a high-quality Neon UI and intelligent double-click detection to switch between running apps and modifying settings.

---
Developed with ⚡ by [Itachi010-a01y](https://github.com/Itachi010-a01y

## ✨ Features

- **Double-Click Logic:** Clever 1.5s time-window to toggle between "Launch Mode" and "Configuration Mode".
- **Neon Aesthetic:** Sleek, dark-mode UI with hover animations and localized content.
- **Auto-Repair:** Automatically detects broken file paths and redirects to settings for an easy fix.
- **State Persistence:** Saves your application paths and language preferences (English, Uzbek, Russian) across sessions.

## 🕹 How It Works (The "Double-Click" Secret)

To keep the interface clean and minimal, the app uses a **time-based execution trigger**:

1.  **Run Apps:** Simply run the app once. It will wait for **1.5 seconds** and then launch your 3 saved applications.
2.  **Edit Settings:** If you need to change your apps, run the program and **quickly run it again (double-click)** within the 1.5s window. The Cyberpunk Control Center will open instantly.



## 🛠 For Developers

### Prerequisites
- Python 3.x
- `tkinter` (usually comes pre-installed with Python)

### How to Compile to EXE
If you want to create your own standalone executable, use the following PyInstaller command:

```bash
python -m PyInstaller --noconfirm --onefile --windowed --icon="logot.ico" --add-data "logot.ico;." AppOpenerX.py
