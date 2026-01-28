import os
import json
import tkinter as tk
from tkinter import messagebox, filedialog
import time
import ctypes
import subprocess
import sys

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

CONFIG_FILE = "config.json"
SETTINGS_FILE = "settings.json"
TEMP_FILE = "running.tmp"
LOCK_FILE = "open.lock"

LANGS = {
    "UZ": {"hdr": "APP OPENER X", "sub1": "TIZIMNI SOZLASH PANELI", "sub2": "BOSHQARUV MARKAZI", "btn": "SAQLASH VA CHIQISH", "app": "ILOVA", "brw": "TANLASH", "err": "Iltimos, ilovani to'g'ri kiriting!"},
    "RU": {"hdr": "APP OPENER X", "sub1": "ПАНЕЛЬ НАСТРОЙКИ", "sub2": "ЦЕНТР УПРАВЛЕНИЯ", "btn": "СОХРАНИТЬ И ВЫЙТИ", "app": "ПРИЛОЖЕНИЕ", "brw": "ВЫБРАТЬ", "err": "Пожалуйста, введите приложение правильно!"},
    "EN": {"hdr": "APP OPENER X", "sub1": "SYSTEM SETUP PANEL", "sub2": "CONTROL CENTER", "btn": "SAVE AND EXIT", "app": "APPLICATION", "brw": "BROWSE", "err": "Please enter the application correctly!"}
}

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_saved_lang():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f).get("lang", "UZ")
        except: pass
    return "UZ"

def run_apps():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try:
                paths = json.load(f)
                for path in paths:
                    clean_path = path.strip().replace('"', '')
                    if clean_path and os.path.exists(clean_path):
                        try: os.startfile(clean_path)
                        except: subprocess.Popen(clean_path, shell=True)
            except: pass
    if os.path.exists(TEMP_FILE):
        try: os.remove(TEMP_FILE)
        except: pass
    sys.exit(0)

def open_settings(first_time=False, error_mode=False):
    with open(LOCK_FILE, "w") as f: f.write("lock")
    if os.path.exists(TEMP_FILE):
        try: os.remove(TEMP_FILE)
        except: pass
        
    root = tk.Tk()
    root.title("App Opener X")
    root.geometry("480x750") 
    root.configure(bg="#0F0F0F")
    root.attributes('-topmost', True)

    icon_path = resource_path("logot.ico")
    if os.path.exists(icon_path):
        try: root.iconbitmap(icon_path)
        except: pass

    curr_lang = get_saved_lang()
    old_paths = []
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                old_paths = json.load(f)
        except: pass

    # --- ASOSIY UI ELEMENTLARINI OLDIN YARATAMIZ ---
    header_frame = tk.Frame(root, bg="#0F0F0F")
    header_frame.pack(pady=(50, 20))
    header_label = tk.Label(header_frame, text="", fg="#00FFCC", bg="#0F0F0F", font=("Helvetica", 24, "bold"))
    header_label.pack()
    sub_label = tk.Label(header_frame, text="", bg="#0F0F0F", font=("Segoe UI", 10))
    sub_label.pack(pady=5)

    entries, labels, browse_btns = [], [], []

    for i in range(1, 4):
        container = tk.Frame(root, bg="#1A1A1A", padx=15, pady=15)
        container.pack(fill="x", padx=35, pady=10)
        l = tk.Label(container, text="", fg="#00FFCC", bg="#1A1A1A", font=("Segoe UI", 8, "bold"))
        l.pack(anchor="w")
        labels.append(l)
        
        input_frame = tk.Frame(container, bg="#1A1A1A")
        input_frame.pack(fill="x", pady=(5, 0))
        en = tk.Entry(input_frame, bg="#1A1A1A", fg="#FFFFFF", insertbackground="#00FFCC", borderwidth=0, font=("Consolas", 10))
        en.pack(side="left", expand=True, fill="x", ipady=5)
        if not error_mode and i-1 < len(old_paths): en.insert(0, old_paths[i-1])
        entries.append(en)
        
        b = tk.Button(input_frame, text="", bg="#1A1A1A", fg="#444444", font=("Segoe UI", 8, "bold"), 
                      borderwidth=0, cursor="hand2", activebackground="#1A1A1A", activeforeground="#00FFCC",
                      command=lambda e=en: e.insert(0, filedialog.askopenfilename() or e.get()))
        b.pack(side="right", padx=(10, 0))
        b.bind("<Enter>", lambda e, btn=b: [btn.config(fg="#00FFCC"), btn.pack_configure(pady=(0, 5))])
        b.bind("<Leave>", lambda e, btn=b: [btn.config(fg="#444444"), btn.pack_configure(pady=0)])
        browse_btns.append(b)
        tk.Frame(container, height=1, bg="#333333").pack(fill="x", pady=(2, 0))

    footer_btn = tk.Button(root, text="", bg="#00FFCC", fg="#000000", font=("Segoe UI", 12, "bold"), width=25, borderwidth=0, cursor="hand2")
    footer_btn.pack(side="bottom", pady=60, ipady=15)

    # --- FUNKSIYALAR ---
    def change_lang(lang):
        nonlocal curr_lang
        curr_lang = lang
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"lang": curr_lang}, f)
        
        L = LANGS[lang]
        header_label.config(text=L["hdr"])
        if error_mode:
            sub_label.config(text=L["err"], fg="#FF4444")
        else:
            sub_label.config(text=L["sub1"] if first_time else L["sub2"], fg="#666666")
        footer_btn.config(text=L["btn"])
        for i, lab in enumerate(labels): lab.config(text=f"{L['app']} #{i+1}")
        for b in browse_btns: b.config(text=L["brw"])

    def save_paths():
        raw_paths = [e.get().strip().replace('"', '') for e in entries if e.get().strip()]
        valid_paths = [p for p in raw_paths if os.path.exists(p)]
        if not raw_paths or len(valid_paths) != len(raw_paths):
            if os.path.exists(CONFIG_FILE): os.remove(CONFIG_FILE)
            with open("error.tmp", "w") as f: f.write("1")
            on_close()
        else:
            with open(CONFIG_FILE, "w") as f: json.dump(valid_paths, f)
            if os.path.exists("error.tmp"): os.remove("error.tmp")
            on_close()

    def on_close():
        if os.path.exists(LOCK_FILE): os.remove(LOCK_FILE)
        root.destroy(); sys.exit(0)

    footer_btn.config(command=save_paths)
    footer_btn.bind("<Enter>", lambda e: footer_btn.config(bg="#1A1A1A", fg="#00FFCC"))
    footer_btn.bind("<Leave>", lambda e: footer_btn.config(bg="#00FFCC", fg="#000000"))

    # Til menyusi
    lang_wrapper = tk.Frame(root, bg="#0F0F0F")
    lang_wrapper.place(x=425, y=10) 
    lang_icon = tk.Label(lang_wrapper, text="🌐", fg="#00FFCC", bg="#0F0F0F", font=("Segoe UI", 18), cursor="hand2")
    lang_icon.pack()

    lang_list = tk.Frame(root, bg="#1A1A1A", bd=1, highlightbackground="#00FFCC", highlightthickness=1)
    for l_code in ["UZ", "RU", "EN"]:
        b = tk.Button(lang_list, text=l_code, fg="#00FFCC", bg="#1A1A1A", font=("Consolas", 10, "bold"), 
                      borderwidth=0, padx=15, pady=8, activebackground="#00FFCC", activeforeground="#000",
                      command=lambda lc=l_code: [change_lang(lc), lang_list.place_forget()])
        b.pack(fill="x")
        b.bind("<Enter>", lambda e, btn=b: btn.config(bg="#00FFCC", fg="#000"))
        b.bind("<Leave>", lambda e, btn=b: btn.config(bg="#1A1A1A", fg="#00FFCC"))

    lang_icon.bind("<Enter>", lambda e: [lang_list.place(x=400, y=55), lang_list.lift()])
    lang_list.bind("<Leave>", lambda e: root.after(150, lambda: lang_list.place_forget() if root.winfo_containing(*root.winfo_pointerxy()) not in [lang_list, lang_icon] else None))

    root.protocol("WM_DELETE_WINDOW", on_close)
    change_lang(curr_lang) # Endi hammasi tayyor bo'lgandan keyin chaqiramiz
    root.mainloop()

if __name__ == "__main__":
    is_error = os.path.exists("error.tmp")
    if is_error:
        try: os.remove("error.tmp")
        except: pass
    
    if not os.path.exists(CONFIG_FILE):
        open_settings(first_time=True, error_mode=is_error)
    else:
        if os.path.exists(TEMP_FILE):
            open_settings(first_time=False)
        else:
            with open(TEMP_FILE, "w") as f: f.write("waiting")
            time.sleep(1.5)
            if os.path.exists(LOCK_FILE):
                if os.path.exists(TEMP_FILE): os.remove(TEMP_FILE)
                sys.exit(0)
            else:
                run_apps()
