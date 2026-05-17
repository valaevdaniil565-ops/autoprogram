import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
import webbrowser
from pathlib import Path
from tkinter import Tk, StringVar, END, SINGLE, filedialog, messagebox, simpledialog, Toplevel, PhotoImage
from tkinter import Listbox
from tkinter import ttk

try:
    import winreg
except ImportError:
    winreg = None

APP_NAME = "StartWork Launcher"
GITHUB_URL = "https://github.com/valaevdaniil565-ops/autoprogram"
RAW_VERSION_URL = "https://raw.githubusercontent.com/valaevdaniil565-ops/autoprogram/main/VERSION"

if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent
else:
    APP_DIR = Path(__file__).resolve().parent

CONFIG_PATH = APP_DIR / "apps.txt"
PROFILES_DIR = APP_DIR / "profiles"
SETTINGS_PATH = APP_DIR / "settings.json"
PROFILE_META_PATH = APP_DIR / "profile_meta.json"
ICON_PATH = APP_DIR / "StartWork.ico"
LOGO_PATH = APP_DIR / "StartWork-icon.png"
VERSION_PATH = APP_DIR / "VERSION"
DEFAULT_PROFILE = "Work"
APP_VERSION = VERSION_PATH.read_text(encoding="utf-8").strip() if VERSION_PATH.exists() else "1.3.0"

BG = "#0f172a"
PANEL = "#172033"
PANEL_LIGHT = "#1f2a44"
TEXT = "#e5e7eb"
MUTED = "#94a3b8"
ACCENT = "#38bdf8"
ACCENT_DARK = "#0ea5e9"
DANGER = "#fb7185"
DANGER_BG = "#3f1d2a"
BORDER = "#334155"
ENTRY = "#0b1220"
PROFILE_ICONS = ["Rocket", "Briefcase", "Home", "Study", "Star", "Tools", "Mail", "Code"]
PROFILE_MARKS = {
    "Rocket": "[>]",
    "Briefcase": "[B]",
    "Home": "[H]",
    "Study": "[S]",
    "Star": "[*]",
    "Tools": "[T]",
    "Mail": "[@]",
    "Code": "[{}]",
}

LANGUAGES = {
    "en": "English",
    "ru": "Русский",
    "zh": "中文",
    "es": "Español",
    "de": "Deutsch",
    "fr": "Français",
    "ja": "日本語",
    "ko": "한국어",
}

TRANSLATIONS = {
    "en": {},
    "ru": {
        "Ready": "Готово",
        "Who is working?": "Кто работает?",
        "Choose a profile. Add your own avatar inside profile settings.": "Выберите профиль. Свой аватар можно добавить в настройках профиля.",
        "New": "Новый",
        "Switch Profile": "Сменить профиль",
        "Profiles, avatars, app library, hotkeys, startup launch, import/export.": "Профили, аватары, библиотека приложений, горячие клавиши, автозапуск, импорт/экспорт.",
        "Profile": "Профиль",
        "Rename": "Переименовать",
        "Avatar": "Аватар",
        "Icon": "Иконка",
        "Delete": "Удалить",
        "Add": "Добавить",
        "Library": "Библиотека",
        "File": "Файл",
        "Folder": "Папка",
        "Link": "Ссылка",
        "Launch Profile": "Запустить профиль",
        "Launch Selected": "Запустить выбранное",
        "Update": "Изменить",
        "Remove": "Убрать",
        "Export": "Экспорт",
        "Import": "Импорт",
        "Save": "Сохранить",
        "Check Updates": "Проверить обновления",
        "About": "О программе",
        "Language": "Язык",
        "Hotkeys: Ctrl+Enter launch, Ctrl+N new, Ctrl+I import, Ctrl+E export, Del remove": "Горячие клавиши: Ctrl+Enter запуск, Ctrl+N новый, Ctrl+I импорт, Ctrl+E экспорт, Del удалить",
        "Welcome": "Добро пожаловать",
        "Create profiles for work, study, personal tasks, then launch everything with one button.": "Создавайте профили для работы, учёбы и личных задач, а потом запускайте всё одной кнопкой.",
        "New profile": "Новый профиль",
        "Profile name:": "Название профиля:",
        "Already exists": "Уже существует",
        "A profile with this name already exists.": "Профиль с таким названием уже существует.",
        "Rename profile": "Переименовать профиль",
        "New name:": "Новое название:",
        "Profile icon": "Иконка профиля",
        "Choose: ": "Выберите: ",
        "Unknown icon": "Неизвестная иконка",
        "Use one of: ": "Используйте одну из: ",
        "Choose avatar image": "Выберите аватар",
        "Cannot delete": "Нельзя удалить",
        "At least one profile must remain.": "Должен остаться хотя бы один профиль.",
        "Delete profile": "Удалить профиль",
        "Empty item": "Пустая строка",
        "Enter an app, path, file, folder, or link.": "Введите приложение, путь, файл, папку или ссылку.",
        "App Library": "Библиотека приложений",
        "Detected apps": "Найденные приложения",
        "Select Telegram, a browser, editor, or Windows tool and add it to this profile.": "Выберите Telegram, браузер, редактор или системный инструмент и добавьте в профиль.",
        "No common apps detected. Use File or Folder instead.": "Стандартные приложения не найдены. Используйте Файл или Папка.",
        "Add Selected": "Добавить выбранное",
        "Add link": "Добавить ссылку",
        "Paste link:": "Вставьте ссылку:",
        "Nothing selected": "Ничего не выбрано",
        "Choose an item to update.": "Выберите строку для изменения.",
        "Enter a new value.": "Введите новое значение.",
        "Saved": "Сохранено",
        "Startup error": "Ошибка автозапуска",
        "Choose an item to launch.": "Выберите строку для запуска.",
        "Launch error": "Ошибка запуска",
        "Empty profile": "Пустой профиль",
        "Add at least one app, file, folder, or link.": "Добавьте хотя бы одно приложение, файл, папку или ссылку.",
        "Some items failed": "Часть элементов не запустилась",
        "Update available": "Доступно обновление",
        "Updates": "Обновления",
        "Update check failed": "Не удалось проверить обновления",
        "Open GitHub?": "Открыть GitHub?",
        "About": "О программе",
        "A one-click launcher for Windows work profiles.": "Лаунчер рабочих профилей Windows в один клик.",
    },
    "zh": {
        "Ready": "就绪", "Who is working?": "谁在使用？", "New": "新建", "Switch Profile": "切换配置", "Profile": "配置", "Rename": "重命名", "Avatar": "头像", "Icon": "图标", "Delete": "删除", "Add": "添加", "Library": "应用库", "File": "文件", "Folder": "文件夹", "Link": "链接", "Launch Profile": "启动配置", "Launch Selected": "启动所选", "Update": "修改", "Remove": "移除", "Export": "导出", "Import": "导入", "Save": "保存", "Check Updates": "检查更新", "About": "关于", "Language": "语言", "Detected apps": "已检测应用", "Add Selected": "添加所选", "App Library": "应用库", "Nothing selected": "未选择", "Empty profile": "配置为空", "Updates": "更新"
    },
    "es": {"Ready": "Listo", "Who is working?": "¿Quién trabaja?", "New": "Nuevo", "Switch Profile": "Cambiar perfil", "Profile": "Perfil", "Rename": "Renombrar", "Avatar": "Avatar", "Delete": "Eliminar", "Add": "Añadir", "Library": "Biblioteca", "File": "Archivo", "Folder": "Carpeta", "Link": "Enlace", "Launch Profile": "Iniciar perfil", "Save": "Guardar", "Language": "Idioma"},
    "de": {"Ready": "Bereit", "Who is working?": "Wer arbeitet?", "New": "Neu", "Switch Profile": "Profil wechseln", "Profile": "Profil", "Rename": "Umbenennen", "Avatar": "Avatar", "Delete": "Löschen", "Add": "Hinzufügen", "Library": "Bibliothek", "File": "Datei", "Folder": "Ordner", "Link": "Link", "Launch Profile": "Profil starten", "Save": "Speichern", "Language": "Sprache"},
    "fr": {"Ready": "Prêt", "Who is working?": "Qui travaille ?", "New": "Nouveau", "Switch Profile": "Changer de profil", "Profile": "Profil", "Rename": "Renommer", "Avatar": "Avatar", "Delete": "Supprimer", "Add": "Ajouter", "Library": "Bibliothèque", "File": "Fichier", "Folder": "Dossier", "Link": "Lien", "Launch Profile": "Lancer le profil", "Save": "Enregistrer", "Language": "Langue"},
    "ja": {"Ready": "準備完了", "Who is working?": "誰が使いますか？", "New": "新規", "Switch Profile": "プロフィール切替", "Profile": "プロフィール", "Rename": "名前変更", "Avatar": "アバター", "Delete": "削除", "Add": "追加", "Library": "ライブラリ", "File": "ファイル", "Folder": "フォルダー", "Link": "リンク", "Launch Profile": "起動", "Save": "保存", "Language": "言語"},
    "ko": {"Ready": "준비됨", "Who is working?": "누가 사용하나요?", "New": "새로 만들기", "Switch Profile": "프로필 변경", "Profile": "프로필", "Rename": "이름 변경", "Avatar": "아바타", "Delete": "삭제", "Add": "추가", "Library": "라이브러리", "File": "파일", "Folder": "폴더", "Link": "링크", "Launch Profile": "프로필 실행", "Save": "저장", "Language": "언어"},
}


def translate(language, text):
    return TRANSLATIONS.get(language, {}).get(text, text)


def load_json(path, default):
    if not path.exists():
        return default.copy() if isinstance(default, dict) else default
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return default.copy() if isinstance(default, dict) else default


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def profile_file_name(name):
    clean = re.sub(r'[<>:"/\\|?*]+', "_", name.strip())
    clean = clean.strip(" .")
    return clean or DEFAULT_PROFILE


def profile_path(name):
    return PROFILES_DIR / f"{profile_file_name(name)}.txt"


def normalize_item(value):
    value = (value or "").strip().strip('"')
    if value.lower().startswith("www."):
        return "https://" + value
    return value


def read_list(path):
    if not path.exists():
        return []
    items = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        value = line.strip().lstrip("\ufeff").strip()
        if value.startswith("п»ї"):
            value = value[3:].lstrip("\ufeff").strip()
        if value and not value.startswith("#"):
            items.append(value)
    return items


def write_list(path, items):
    header = [
        "# StartWorkLauncher apps list",
        "# One app, folder, file, or URL per line.",
        "",
    ]
    path.parent.mkdir(exist_ok=True)
    path.write_text("\n".join(header + items) + "\n", encoding="utf-8")


def ensure_profiles():
    PROFILES_DIR.mkdir(exist_ok=True)
    if not any(PROFILES_DIR.glob("*.txt")):
        write_list(PROFILES_DIR / f"{DEFAULT_PROFILE}.txt", [])
    if not CONFIG_PATH.exists():
        write_list(CONFIG_PATH, [])


def list_profiles():
    ensure_profiles()
    names = [path.stem for path in sorted(PROFILES_DIR.glob("*.txt"), key=lambda item: item.stem.lower())]
    if DEFAULT_PROFILE in names:
        names.remove(DEFAULT_PROFILE)
        names.insert(0, DEFAULT_PROFILE)
    return names or [DEFAULT_PROFILE]


def launch_item(item):
    try:
        if item.startswith(("http://", "https://", "mailto:")):
            webbrowser.open(item)
            return True, None
        if os.path.exists(item):
            os.startfile(item)
            return True, None
        subprocess.Popen(item, shell=True)
        return True, None
    except Exception as exc:
        return False, str(exc)


def candidate_paths(*parts):
    roots = [
        os.environ.get("ProgramFiles", ""),
        os.environ.get("ProgramFiles(x86)", ""),
        os.environ.get("LOCALAPPDATA", ""),
        os.environ.get("APPDATA", ""),
        os.environ.get("WINDIR", ""),
    ]
    return [str(Path(root, *parts)) for root in roots if root]


def command_exists(command):
    from shutil import which
    return which(command) is not None


def detect_app_library():
    curated = [
        ("Google Chrome", candidate_paths("Google", "Chrome", "Application", "chrome.exe")),
        ("Microsoft Edge", candidate_paths("Microsoft", "Edge", "Application", "msedge.exe")),
        ("Mozilla Firefox", candidate_paths("Mozilla Firefox", "firefox.exe")),
        ("Brave Browser", candidate_paths("BraveSoftware", "Brave-Browser", "Application", "brave.exe")),
        ("Opera", candidate_paths("Programs", "Opera", "opera.exe")),
        ("Telegram", [str(Path(os.environ.get("APPDATA", ""), "Telegram Desktop", "Telegram.exe"))]),
        ("Discord", [str(Path(os.environ.get("LOCALAPPDATA", ""), "Discord", "Update.exe"))]),
        ("Steam", candidate_paths("Steam", "steam.exe")),
        ("Visual Studio Code", [str(Path(os.environ.get("LOCALAPPDATA", ""), "Programs", "Microsoft VS Code", "Code.exe"))] + candidate_paths("Microsoft VS Code", "Code.exe")),
        ("Notepad", ["notepad"]),
        ("Calculator", ["calc"]),
        ("Paint", ["mspaint"]),
        ("File Explorer", ["explorer"]),
    ]
    found = []
    seen = set()
    for name, paths in curated:
        for path in paths:
            if not path:
                continue
            if os.path.exists(path) or ("\\" not in path and "/" not in path and command_exists(path)):
                key = (name.lower(), path.lower())
                if key not in seen:
                    found.append({"name": name, "path": path})
                    seen.add(key)
                break
    return found


def command_for_startup():
    if getattr(sys, "frozen", False):
        return f'"{sys.executable}"'
    return f'"{sys.executable}" "{Path(__file__).resolve()}"'


def is_startup_enabled():
    if winreg is None:
        return False
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run") as key:
            value, _ = winreg.QueryValueEx(key, APP_NAME)
            return bool(value)
    except OSError:
        return False


def set_startup_enabled(enabled):
    if winreg is None:
        raise RuntimeError("Windows startup registry is not available on this system.")
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE) as key:
        if enabled:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, command_for_startup())
        else:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass


class StartWorkApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} {APP_VERSION}")
        self.root.geometry("960x640")
        self.root.minsize(820, 560)
        self.root.configure(bg=BG)

        if ICON_PATH.exists():
            try:
                self.root.iconbitmap(str(ICON_PATH))
            except Exception:
                pass

        ensure_profiles()
        self.settings = load_json(SETTINGS_PATH, {"first_run_done": False, "startup_launch_profile": "", "auto_launch_on_start": False})
        self.profile_meta = load_json(PROFILE_META_PATH, {})
        self.profiles = list_profiles()
        self.active_profile = DEFAULT_PROFILE if DEFAULT_PROFILE in self.profiles else self.profiles[0]
        self.profile_var = StringVar(value=self.display_profile(self.active_profile))
        self.entry_var = StringVar()
        self.language_var = StringVar(value=self.settings.get("language", "en"))
        self.status_var = StringVar(value=self.t("Ready"))
        self.items = []
        self.images = {}

        self.setup_style()
        self.show_profile_selector()
        self.maybe_auto_launch()

    @property
    def current_profile_path(self):
        return profile_path(self.active_profile)

    def t(self, text):
        return translate(self.language_var.get() if hasattr(self, "language_var") else self.settings.get("language", "en"), text)

    def set_language(self, _event=None):
        selected = self.language_var.get()
        code = selected.split(" - ", 1)[0] if " - " in selected else selected
        if code not in LANGUAGES:
            for key, label in LANGUAGES.items():
                if label == selected:
                    code = key
                    break
        self.settings["language"] = code
        save_json(SETTINGS_PATH, self.settings)
        self.language_var.set(code)
        if hasattr(self, "listbox"):
            self.build_ui()
            self.load_profile(self.active_profile, save_current=False)
        else:
            self.show_profile_selector()

    def add_language_selector(self, parent):
        ttk.Label(parent, text=self.t("Language"), style="Panel.TLabel").pack(side="left", padx=(12, 6))
        values = [f"{code} - {label}" for code, label in LANGUAGES.items()]
        code = self.settings.get("language", self.language_var.get() or "en")
        self.language_var.set(f"{code} - {LANGUAGES.get(code, code)}")
        box = ttk.Combobox(parent, textvariable=self.language_var, values=values, state="readonly", width=16)
        box.pack(side="left")
        box.bind("<<ComboboxSelected>>", self.set_language)
        return box

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL, relief="flat")
        style.configure("Toolbar.TFrame", background=PANEL)
        style.configure("TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=BG, foreground=TEXT, font=("Segoe UI Semibold", 24))
        style.configure("Muted.TLabel", background=BG, foreground=MUTED, font=("Segoe UI", 10))
        style.configure("Panel.TLabel", background=PANEL, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Status.TLabel", background=PANEL, foreground=MUTED, font=("Segoe UI", 9))
        style.configure("TEntry", fieldbackground=ENTRY, foreground=TEXT, insertcolor=TEXT, bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER, padding=10)
        style.configure("TCombobox", fieldbackground=ENTRY, background=PANEL_LIGHT, foreground=TEXT, arrowcolor=TEXT, bordercolor=BORDER, padding=8)
        style.map("TCombobox", fieldbackground=[("readonly", ENTRY)], foreground=[("readonly", TEXT)])
        style.configure("TButton", background=PANEL_LIGHT, foreground=TEXT, font=("Segoe UI Semibold", 10), padding=(12, 9), borderwidth=0, focusthickness=0)
        style.map("TButton", background=[("active", "#263653")], foreground=[("active", TEXT)])
        style.configure("Primary.TButton", background=ACCENT_DARK, foreground="#ffffff")
        style.map("Primary.TButton", background=[("active", ACCENT)])
        style.configure("Danger.TButton", background=DANGER_BG, foreground="#fecdd3")
        style.map("Danger.TButton", background=[("active", "#5f2435")])
        style.configure("Vertical.TScrollbar", background=PANEL_LIGHT, troughcolor=PANEL, bordercolor=PANEL, arrowcolor=TEXT)

    def clear_root(self):
        for child in self.root.winfo_children():
            child.destroy()

    def get_avatar_image(self, profile, size=96):
        meta = self.profile_meta.get(profile, {})
        avatar = meta.get("avatar")
        path = Path(avatar) if avatar else LOGO_PATH
        if not path.exists():
            path = LOGO_PATH
        key = f"{profile}:{path}:{size}"
        try:
            image = PhotoImage(file=str(path))
            factor = max(1, image.width() // size, image.height() // size)
            if factor > 1:
                image = image.subsample(factor, factor)
            self.images[key] = image
            return image
        except Exception:
            return None

    def show_profile_selector(self):
        self.clear_root()
        self.images.clear()
        wrap = ttk.Frame(self.root, padding=28)
        wrap.pack(fill="both", expand=True)
        top = ttk.Frame(wrap)
        top.pack(fill="x")
        logo = self.get_avatar_image("__logo__", 56)
        if logo:
            ttk.Label(top, image=logo, background=BG).pack(side="left", padx=(0, 12))
        ttk.Label(top, text=APP_NAME, style="Title.TLabel").pack(side="left")
        self.add_language_selector(top)
        ttk.Button(top, text="X", command=self.root.destroy).pack(side="right")

        center = ttk.Frame(wrap)
        center.pack(expand=True)
        ttk.Label(center, text=self.t("Who is working?"), style="Title.TLabel").pack(pady=(0, 28))
        tiles = ttk.Frame(center)
        tiles.pack()
        self.profiles = list_profiles()
        for profile in self.profiles:
            self.profile_tile(tiles, profile).pack(side="left", padx=12)
        self.add_profile_tile(tiles).pack(side="left", padx=12)
        ttk.Label(center, text=self.t("Choose a profile. Add your own avatar inside profile settings."), style="Muted.TLabel").pack(pady=(24, 0))

    def profile_tile(self, parent, profile):
        frame = ttk.Frame(parent, style="Panel.TFrame", padding=10)
        image = self.get_avatar_image(profile, 96)
        if image:
            label = ttk.Label(frame, image=image, background=PANEL)
        else:
            label = ttk.Label(frame, text=self.display_profile(profile).split(" ")[0], style="Panel.TLabel", font=("Segoe UI Semibold", 24))
        label.pack()
        name = ttk.Label(frame, text=profile, style="Panel.TLabel")
        name.pack(pady=(8, 0))
        for widget in (frame, label, name):
            widget.bind("<Button-1>", lambda _event, p=profile: self.open_profile(p))
        return frame

    def add_profile_tile(self, parent):
        frame = ttk.Frame(parent, style="Panel.TFrame", padding=18)
        plus = ttk.Label(frame, text="+", style="Panel.TLabel", font=("Segoe UI Semibold", 48))
        plus.pack()
        name = ttk.Label(frame, text=self.t("New"), style="Panel.TLabel")
        name.pack(pady=(8, 0))
        for widget in (frame, plus, name):
            widget.bind("<Button-1>", lambda _event: self.create_profile(from_selector=True))
        return frame

    def open_profile(self, profile):
        self.active_profile = profile
        self.build_ui()
        self.bind_hotkeys()
        self.load_profile(profile, save_current=False)
        self.run_first_launch_wizard()

    def build_ui(self):
        self.clear_root()
        outer = ttk.Frame(self.root, padding=24)
        outer.pack(fill="both", expand=True)
        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 18))
        logo = self.get_avatar_image(self.active_profile, 48)
        if logo:
            ttk.Label(header, image=logo, background=BG).pack(side="left", padx=(0, 12))
        title_box = ttk.Frame(header)
        title_box.pack(side="left")
        ttk.Label(title_box, text=APP_NAME, style="Title.TLabel").pack(anchor="w")
        ttk.Label(title_box, text=self.t("Profiles, avatars, app library, hotkeys, startup launch, import/export."), style="Muted.TLabel").pack(anchor="w", pady=(5, 0))
        self.add_language_selector(header)
        ttk.Button(header, text=self.t("Switch Profile"), command=self.show_profile_selector).pack(side="right")

        content = ttk.Frame(outer, style="Panel.TFrame", padding=18)
        content.pack(fill="both", expand=True)

        profile_row = ttk.Frame(content, style="Toolbar.TFrame")
        profile_row.pack(fill="x", pady=(0, 12))
        ttk.Label(profile_row, text=self.t("Profile"), style="Panel.TLabel").pack(side="left", padx=(0, 10))
        self.profile_box = ttk.Combobox(profile_row, textvariable=self.profile_var, values=self.display_profiles(), state="readonly", width=28)
        self.profile_box.pack(side="left")
        self.profile_box.bind("<<ComboboxSelected>>", self.on_profile_selected)
        ttk.Button(profile_row, text=self.t("New"), command=self.create_profile).pack(side="left", padx=(10, 0))
        ttk.Button(profile_row, text=self.t("Rename"), command=self.rename_profile).pack(side="left", padx=(8, 0))
        ttk.Button(profile_row, text=self.t("Avatar"), command=self.change_profile_avatar).pack(side="left", padx=(8, 0))
        ttk.Button(profile_row, text=self.t("Icon"), command=self.change_profile_icon).pack(side="left", padx=(8, 0))
        ttk.Button(profile_row, text=self.t("Delete"), style="Danger.TButton", command=self.delete_profile).pack(side="left", padx=(8, 0))

        input_row = ttk.Frame(content, style="Toolbar.TFrame")
        input_row.pack(fill="x", pady=(0, 12))
        self.entry = ttk.Entry(input_row, textvariable=self.entry_var)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda _event: self.add_item())
        ttk.Button(input_row, text=self.t("Add"), style="Primary.TButton", command=self.add_item).pack(side="left", padx=(10, 0))
        ttk.Button(input_row, text=self.t("Library"), command=self.open_app_library).pack(side="left", padx=(8, 0))
        ttk.Button(input_row, text=self.t("File"), command=self.pick_file).pack(side="left", padx=(8, 0))
        ttk.Button(input_row, text=self.t("Folder"), command=self.pick_folder).pack(side="left", padx=(8, 0))
        ttk.Button(input_row, text=self.t("Link"), command=self.add_link_from_dialog).pack(side="left", padx=(8, 0))

        list_frame = ttk.Frame(content, style="Panel.TFrame")
        list_frame.pack(fill="both", expand=True)
        self.listbox = Listbox(list_frame, selectmode=SINGLE, activestyle="none", bg=ENTRY, fg=TEXT, selectbackground=ACCENT_DARK, selectforeground="#ffffff", highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT, relief="flat", borderwidth=0, font=("Segoe UI", 11), height=12)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.bind("<Double-Button-1>", lambda _event: self.launch_selected())
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview, style="Vertical.TScrollbar")
        scrollbar.pack(side="right", fill="y")
        self.listbox.configure(yscrollcommand=scrollbar.set)

        actions = ttk.Frame(content, style="Toolbar.TFrame")
        actions.pack(fill="x", pady=(14, 0))
        ttk.Button(actions, text=self.t("Launch Profile"), style="Primary.TButton", command=self.launch_all).pack(side="left")
        ttk.Button(actions, text=self.t("Launch Selected"), command=self.launch_selected).pack(side="left", padx=(8, 0))
        ttk.Button(actions, text=self.t("Update"), command=self.update_selected).pack(side="left", padx=(8, 0))
        ttk.Button(actions, text=self.t("Remove"), style="Danger.TButton", command=self.delete_selected).pack(side="left", padx=(8, 0))
        ttk.Button(actions, text=self.t("Export"), command=self.export_profile).pack(side="right")
        ttk.Button(actions, text=self.t("Import"), command=self.import_profile).pack(side="right", padx=(0, 8))
        ttk.Button(actions, text=self.t("Save"), command=self.save).pack(side="right", padx=(0, 8))

        utility = ttk.Frame(content, style="Toolbar.TFrame")
        utility.pack(fill="x", pady=(10, 0))
        ttk.Button(utility, text="Startup: Off", command=self.toggle_startup).pack(side="left")
        self.startup_button = utility.winfo_children()[0]
        ttk.Button(utility, text=self.t("Check Updates"), command=self.check_updates).pack(side="left", padx=(8, 0))
        ttk.Button(utility, text=self.t("About"), command=self.show_about).pack(side="left", padx=(8, 0))
        ttk.Label(utility, text=self.t("Hotkeys: Ctrl+Enter launch, Ctrl+N new, Ctrl+I import, Ctrl+E export, Del remove"), style="Status.TLabel").pack(side="right")

        ttk.Label(content, textvariable=self.status_var, style="Status.TLabel").pack(anchor="w", pady=(12, 0))
        self.refresh_startup_button()

    def bind_hotkeys(self):
        self.root.bind("<Control-Return>", lambda _event: self.launch_all())
        self.root.bind("<Control-n>", lambda _event: self.create_profile())
        self.root.bind("<Control-i>", lambda _event: self.import_profile())
        self.root.bind("<Control-e>", lambda _event: self.export_profile())
        self.root.bind("<Delete>", lambda _event: self.delete_selected())
        self.root.bind("<F5>", lambda _event: self.save(show_message=False))

    def display_profile(self, name):
        icon = self.profile_meta.get(name, {}).get("icon", "Rocket")
        return f"{PROFILE_MARKS.get(icon, '[>]')} {name}"

    def display_profiles(self):
        return [self.display_profile(name) for name in self.profiles]

    def profile_from_display(self, value):
        for name in self.profiles:
            if value.endswith(name):
                return name
        return self.active_profile

    def reload_profiles(self):
        self.profiles = list_profiles()
        self.profile_box.configure(values=self.display_profiles())

    def load_profile(self, profile_name, save_current=True):
        if save_current and hasattr(self, "items"):
            write_list(profile_path(self.active_profile), self.items)
        self.active_profile = profile_name
        self.profile_var.set(self.display_profile(profile_name))
        self.items = read_list(self.current_profile_path)
        self.entry_var.set("")
        self.refresh_list()
        self.sync_legacy_config()

    def on_profile_selected(self, _event=None):
        self.load_profile(self.profile_from_display(self.profile_var.get()))

    def run_first_launch_wizard(self):
        if self.settings.get("first_run_done"):
            return
        messagebox.showinfo("Welcome", "Create profiles for work, study, personal tasks, then launch everything with one button.")
        name = simpledialog.askstring("First profile", "Profile name:", initialvalue=DEFAULT_PROFILE, parent=self.root)
        if name:
            clean = profile_file_name(name)
            if clean != self.active_profile and not profile_path(clean).exists():
                profile_path(self.active_profile).rename(profile_path(clean))
                self.reload_profiles()
                self.load_profile(clean, save_current=False)
        self.settings["first_run_done"] = True
        save_json(SETTINGS_PATH, self.settings)

    def maybe_auto_launch(self):
        profile = self.settings.get("startup_launch_profile")
        if self.settings.get("auto_launch_on_start") and profile in self.profiles:
            self.open_profile(profile)
            self.root.after(800, self.launch_all)

    def create_profile(self, from_selector=False):
        name = simpledialog.askstring("New profile", "Profile name:", parent=self.root)
        if not name:
            return
        clean = profile_file_name(name)
        path = profile_path(clean)
        if path.exists():
            messagebox.showwarning("Already exists", "A profile with this name already exists.")
            return
        write_list(path, [])
        self.profile_meta.setdefault(clean, {"icon": "Rocket"})
        save_json(PROFILE_META_PATH, self.profile_meta)
        self.reload_profiles()
        if from_selector:
            self.show_profile_selector()
        else:
            self.load_profile(clean)

    def rename_profile(self):
        old_name = self.active_profile
        new_name = simpledialog.askstring("Rename profile", "New name:", initialvalue=old_name, parent=self.root)
        if not new_name:
            return
        clean = profile_file_name(new_name)
        old_path = profile_path(old_name)
        new_path = profile_path(clean)
        if new_path.exists() and new_path != old_path:
            messagebox.showwarning("Already exists", "A profile with this name already exists.")
            return
        self.save(show_message=False)
        old_path.rename(new_path)
        if old_name in self.profile_meta:
            self.profile_meta[clean] = self.profile_meta.pop(old_name)
            save_json(PROFILE_META_PATH, self.profile_meta)
        self.reload_profiles()
        self.load_profile(clean, save_current=False)

    def change_profile_icon(self):
        choice = simpledialog.askstring("Profile icon", "Choose: " + ", ".join(PROFILE_ICONS), initialvalue=self.profile_meta.get(self.active_profile, {}).get("icon", "Rocket"), parent=self.root)
        if not choice:
            return
        choice = choice.strip().title()
        if choice not in PROFILE_ICONS:
            messagebox.showwarning("Unknown icon", "Use one of: " + ", ".join(PROFILE_ICONS))
            return
        self.profile_meta.setdefault(self.active_profile, {})["icon"] = choice
        save_json(PROFILE_META_PATH, self.profile_meta)
        self.reload_profiles()
        self.profile_var.set(self.display_profile(self.active_profile))

    def change_profile_avatar(self):
        path = filedialog.askopenfilename(title="Choose avatar image", filetypes=[("PNG/GIF images", "*.png *.gif"), ("All files", "*.*")])
        if not path:
            return
        self.profile_meta.setdefault(self.active_profile, {})["avatar"] = path
        save_json(PROFILE_META_PATH, self.profile_meta)
        self.build_ui()
        self.load_profile(self.active_profile, save_current=False)

    def delete_profile(self):
        if len(self.profiles) <= 1:
            messagebox.showwarning("Cannot delete", "At least one profile must remain.")
            return
        if not messagebox.askyesno("Delete profile", f"Delete profile '{self.active_profile}'?"):
            return
        self.current_profile_path.unlink(missing_ok=True)
        self.profile_meta.pop(self.active_profile, None)
        save_json(PROFILE_META_PATH, self.profile_meta)
        self.reload_profiles()
        self.load_profile(self.profiles[0], save_current=False)

    def refresh_list(self):
        self.listbox.delete(0, END)
        for item in self.items:
            self.listbox.insert(END, item)
        self.status_var.set(f"{self.t("Profile")}: {self.active_profile}. Items: {len(self.items)}")

    def sync_legacy_config(self):
        write_list(CONFIG_PATH, self.items)

    def selected_index(self):
        selection = self.listbox.curselection()
        return selection[0] if selection else None

    def on_select(self, _event=None):
        index = self.selected_index()
        if index is not None:
            self.entry_var.set(self.items[index])

    def add_item(self):
        value = normalize_item(self.entry_var.get())
        if not value:
            messagebox.showwarning("Empty item", "Enter an app, path, file, folder, or link.")
            return
        self.items.append(value)
        self.entry_var.set("")
        self.save(show_message=False)
        self.refresh_list()
        self.status_var.set(f"Added: {value}")

    def open_app_library(self):
        apps = detect_app_library()
        win = Toplevel(self.root)
        win.title("App Library")
        win.geometry("700x440")
        win.configure(bg=BG)
        ttk.Label(win, text=self.t("Detected apps"), style="Title.TLabel").pack(anchor="w", padx=18, pady=(18, 6))
        ttk.Label(win, text=self.t("Select Telegram, a browser, editor, or Windows tool and add it to this profile."), style="Muted.TLabel").pack(anchor="w", padx=18, pady=(0, 12))
        frame = ttk.Frame(win, style="Panel.TFrame", padding=14)
        frame.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        box = Listbox(frame, bg=ENTRY, fg=TEXT, selectbackground=ACCENT_DARK, selectforeground="#ffffff", relief="flat", font=("Segoe UI", 10), height=12)
        box.pack(fill="both", expand=True)
        if apps:
            for app in apps:
                box.insert(END, f"{app['name']}    |    {app['path']}")
        else:
            box.insert(END, "No common apps detected. Use File or Folder instead.")

        def add_selected():
            selection = box.curselection()
            if not selection or not apps:
                return
            item = apps[selection[0]]["path"]
            self.items.append(item)
            self.save(show_message=False)
            self.refresh_list()
            win.destroy()

        ttk.Button(frame, text=self.t("Add Selected"), style="Primary.TButton", command=add_selected).pack(anchor="e", pady=(12, 0))

    def add_link_from_dialog(self):
        value = simpledialog.askstring("Add link", "Paste link:", parent=self.root)
        value = normalize_item(value)
        if not value:
            return
        if not value.lower().startswith(("http://", "https://", "mailto:")):
            value = "https://" + value
        self.entry_var.set(value)
        self.add_item()

    def update_selected(self):
        index = self.selected_index()
        if index is None:
            messagebox.showinfo("Nothing selected", "Choose an item to update.")
            return
        value = normalize_item(self.entry_var.get())
        if not value:
            messagebox.showwarning("Empty item", "Enter a new value.")
            return
        self.items[index] = value
        self.save(show_message=False)
        self.refresh_list()
        self.listbox.selection_set(index)

    def delete_selected(self):
        index = self.selected_index()
        if index is None:
            return
        removed = self.items.pop(index)
        self.entry_var.set("")
        self.save(show_message=False)
        self.refresh_list()
        self.status_var.set(f"Removed: {removed}")

    def pick_file(self):
        path = filedialog.askopenfilename(title="Choose app or file")
        if path:
            self.entry_var.set(path)

    def pick_folder(self):
        path = filedialog.askdirectory(title="Choose folder")
        if path:
            self.entry_var.set(path)

    def save(self, show_message=True):
        write_list(self.current_profile_path, self.items)
        self.sync_legacy_config()
        self.status_var.set("Profile saved")
        if show_message:
            messagebox.showinfo("Saved", f"Profile saved: {self.active_profile}")

    def import_profile(self):
        path = filedialog.askopenfilename(title="Import profile", filetypes=[("Profile files", "*.txt *.json"), ("All files", "*.*")])
        if not path:
            return
        source = Path(path)
        name = profile_file_name(source.stem)
        target = profile_path(name)
        counter = 2
        while target.exists():
            name = f"{profile_file_name(source.stem)} {counter}"
            target = profile_path(name)
            counter += 1
        if source.suffix.lower() == ".json":
            data = load_json(source, {})
            items = data.get("items", []) if isinstance(data, dict) else []
        else:
            items = read_list(source)
        write_list(target, items)
        self.reload_profiles()
        self.load_profile(name)

    def export_profile(self):
        path = filedialog.asksaveasfilename(title="Export profile", initialfile=f"{self.active_profile}.txt", defaultextension=".txt", filetypes=[("Text profile", "*.txt"), ("JSON profile", "*.json")])
        if not path:
            return
        target = Path(path)
        if target.suffix.lower() == ".json":
            save_json(target, {"name": self.active_profile, "version": APP_VERSION, "items": self.items})
        else:
            write_list(target, self.items)
        self.status_var.set(f"Exported: {target.name}")

    def refresh_startup_button(self):
        enabled = is_startup_enabled()
        self.startup_button.configure(text="Startup: On" if enabled else "Startup: Off")

    def toggle_startup(self):
        try:
            next_state = not is_startup_enabled()
            set_startup_enabled(next_state)
            self.settings["auto_launch_on_start"] = next_state
            self.settings["startup_launch_profile"] = self.active_profile if next_state else ""
            save_json(SETTINGS_PATH, self.settings)
            self.refresh_startup_button()
            self.status_var.set("Windows startup enabled" if next_state else "Windows startup disabled")
        except Exception as exc:
            messagebox.showerror("Startup error", str(exc))

    def launch_selected(self):
        index = self.selected_index()
        if index is None:
            messagebox.showinfo("Nothing selected", "Choose an item to launch.")
            return
        item = self.items[index]
        ok, error = launch_item(item)
        self.status_var.set(f"Launched: {item}" if ok else f"Launch error: {item}")
        if not ok:
            messagebox.showerror("Launch error", error or item)

    def launch_all(self):
        if not self.items:
            messagebox.showinfo("Empty profile", "Add at least one app, file, folder, or link.")
            return
        self.save(show_message=False)
        errors = []
        for item in self.items:
            ok, error = launch_item(item)
            if not ok:
                errors.append(f"{item}: {error}")
        if errors:
            messagebox.showerror("Some items failed", "\n".join(errors))
            self.status_var.set(f"Launched with errors: {len(errors)}")
        else:
            self.status_var.set(f"Launched profile '{self.active_profile}': {len(self.items)}")

    def check_updates(self):
        try:
            with urllib.request.urlopen(RAW_VERSION_URL, timeout=5) as response:
                latest = response.read().decode("utf-8").strip()
            if latest and latest != APP_VERSION:
                if messagebox.askyesno("Update available", f"Current: {APP_VERSION}\nLatest: {latest}\nOpen GitHub?"):
                    webbrowser.open(GITHUB_URL)
            else:
                messagebox.showinfo("Updates", f"You are using the latest version: {APP_VERSION}")
        except Exception as exc:
            messagebox.showerror("Update check failed", str(exc))

    def show_about(self):
        messagebox.showinfo("About", f"{APP_NAME}\nVersion {APP_VERSION}\n\nA one-click launcher for Windows work profiles.\n\n{GITHUB_URL}")


def main():
    root = Tk()
    StartWorkApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
