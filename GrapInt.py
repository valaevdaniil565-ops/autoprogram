import os
import re
import subprocess
import sys
import webbrowser
from pathlib import Path
from tkinter import Tk, StringVar, END, SINGLE, filedialog, messagebox, simpledialog
from tkinter import Listbox
from tkinter import ttk

if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent
else:
    APP_DIR = Path(__file__).resolve().parent
CONFIG_PATH = APP_DIR / "apps.txt"
PROFILES_DIR = APP_DIR / "profiles"
ICON_PATH = APP_DIR / "StartWork.ico"
DEFAULT_PROFILE = "Работа"

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


def profile_file_name(name):
    clean = re.sub(r'[<>:"/\\|?*]+', "_", name.strip())
    clean = clean.strip(" .")
    return clean or DEFAULT_PROFILE


def profile_path(name):
    return PROFILES_DIR / f"{profile_file_name(name)}.txt"


def normalize_item(value):
    value = value.strip()
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
    path.write_text("\n".join(header + items) + "\n", encoding="utf-8")


def ensure_profiles():
    PROFILES_DIR.mkdir(exist_ok=True)
    existing = sorted(PROFILES_DIR.glob("*.txt"))
    if existing:
        return

    old_items = read_list(CONFIG_PATH)
    write_list(PROFILES_DIR / f"{DEFAULT_PROFILE}.txt", old_items)
    write_list(PROFILES_DIR / "Личное.txt", [])
    write_list(PROFILES_DIR / "Учёба.txt", [])


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


class StartWorkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StartWork Launcher")
        self.root.geometry("860x590")
        self.root.minsize(760, 520)
        self.root.configure(bg=BG)

        if ICON_PATH.exists():
            try:
                self.root.iconbitmap(str(ICON_PATH))
            except Exception:
                pass

        self.profiles = list_profiles()
        self.active_profile = DEFAULT_PROFILE if DEFAULT_PROFILE in self.profiles else self.profiles[0]
        self.profile_var = StringVar(value=self.active_profile)
        self.entry_var = StringVar()
        self.status_var = StringVar(value="Готов к запуску")
        self.items = []

        self.setup_style()
        self.build_ui()
        self.load_profile(self.profile_var.get(), save_current=False)

    @property
    def current_profile_path(self):
        return profile_path(self.active_profile)

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
        style.configure("TButton", background=PANEL_LIGHT, foreground=TEXT, font=("Segoe UI Semibold", 10), padding=(14, 10), borderwidth=0, focusthickness=0)
        style.map("TButton", background=[("active", "#263653")], foreground=[("active", TEXT)])
        style.configure("Primary.TButton", background=ACCENT_DARK, foreground="#ffffff")
        style.map("Primary.TButton", background=[("active", ACCENT)])
        style.configure("Danger.TButton", background=DANGER_BG, foreground="#fecdd3")
        style.map("Danger.TButton", background=[("active", "#5f2435")])
        style.configure("Vertical.TScrollbar", background=PANEL_LIGHT, troughcolor=PANEL, bordercolor=PANEL, arrowcolor=TEXT)

    def build_ui(self):
        outer = ttk.Frame(self.root, padding=24)
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 18))
        ttk.Label(header, text="StartWork Launcher", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Профили запуска для разных сценариев: работа, личное, учёба или свой набор.", style="Muted.TLabel").pack(anchor="w", pady=(5, 0))

        content = ttk.Frame(outer, style="Panel.TFrame", padding=18)
        content.pack(fill="both", expand=True)

        profile_row = ttk.Frame(content, style="Toolbar.TFrame")
        profile_row.pack(fill="x", pady=(0, 14))
        ttk.Label(profile_row, text="Профиль", style="Panel.TLabel").pack(side="left", padx=(0, 10))

        self.profile_box = ttk.Combobox(profile_row, textvariable=self.profile_var, values=self.profiles, state="readonly", width=24)
        self.profile_box.pack(side="left")
        self.profile_box.bind("<<ComboboxSelected>>", self.on_profile_selected)

        ttk.Button(profile_row, text="Новый", command=self.create_profile).pack(side="left", padx=(10, 0))
        ttk.Button(profile_row, text="Переименовать", command=self.rename_profile).pack(side="left", padx=(8, 0))
        ttk.Button(profile_row, text="Удалить профиль", style="Danger.TButton", command=self.delete_profile).pack(side="left", padx=(8, 0))

        input_row = ttk.Frame(content, style="Toolbar.TFrame")
        input_row.pack(fill="x", pady=(0, 14))
        self.entry = ttk.Entry(input_row, textvariable=self.entry_var)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda _event: self.add_item())
        ttk.Button(input_row, text="Добавить", style="Primary.TButton", command=self.add_item).pack(side="left", padx=(10, 0))
        ttk.Button(input_row, text="Файл", command=self.pick_file).pack(side="left", padx=(8, 0))
        ttk.Button(input_row, text="Папка", command=self.pick_folder).pack(side="left", padx=(8, 0))
        ttk.Button(input_row, text="Ссылка", command=self.add_link_from_dialog).pack(side="left", padx=(8, 0))

        list_frame = ttk.Frame(content, style="Panel.TFrame")
        list_frame.pack(fill="both", expand=True)
        self.listbox = Listbox(
            list_frame,
            selectmode=SINGLE,
            activestyle="none",
            bg=ENTRY,
            fg=TEXT,
            selectbackground=ACCENT_DARK,
            selectforeground="#ffffff",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 11),
            height=12,
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.bind("<Double-Button-1>", lambda _event: self.launch_selected())

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview, style="Vertical.TScrollbar")
        scrollbar.pack(side="right", fill="y")
        self.listbox.configure(yscrollcommand=scrollbar.set)

        actions = ttk.Frame(content, style="Toolbar.TFrame")
        actions.pack(fill="x", pady=(14, 0))
        ttk.Button(actions, text="Запустить профиль", style="Primary.TButton", command=self.launch_all).pack(side="left")
        ttk.Button(actions, text="Запустить выбранное", command=self.launch_selected).pack(side="left", padx=(8, 0))
        ttk.Button(actions, text="Изменить", command=self.update_selected).pack(side="left", padx=(8, 0))
        ttk.Button(actions, text="Удалить", style="Danger.TButton", command=self.delete_selected).pack(side="left", padx=(8, 0))
        ttk.Button(actions, text="Сохранить", command=self.save).pack(side="right")

        ttk.Label(content, textvariable=self.status_var, style="Status.TLabel").pack(anchor="w", pady=(12, 0))

    def reload_profiles(self):
        self.profiles = list_profiles()
        self.profile_box.configure(values=self.profiles)

    def load_profile(self, profile_name, save_current=True):
        if save_current and hasattr(self, "items"):
            write_list(profile_path(self.active_profile), self.items)
        self.active_profile = profile_name
        self.profile_var.set(profile_name)
        self.items = read_list(self.current_profile_path)
        self.entry_var.set("")
        self.refresh_list()
        self.sync_legacy_config()
        self.status_var.set(f"Профиль: {profile_name}. В списке: {len(self.items)}")

    def on_profile_selected(self, _event=None):
        self.load_profile(self.profile_var.get())

    def create_profile(self):
        name = simpledialog.askstring("Новый профиль", "Название профиля:", parent=self.root)
        if not name:
            return
        clean = profile_file_name(name)
        path = PROFILES_DIR / f"{clean}.txt"
        if path.exists():
            messagebox.showwarning("Уже есть", "Профиль с таким названием уже существует.")
            return
        write_list(path, [])
        self.reload_profiles()
        self.load_profile(clean)

    def rename_profile(self):
        old_name = self.active_profile
        new_name = simpledialog.askstring("Переименовать профиль", "Новое название:", initialvalue=old_name, parent=self.root)
        if not new_name:
            return
        old_path = profile_path(old_name)
        clean = profile_file_name(new_name)
        new_path = PROFILES_DIR / f"{clean}.txt"
        if new_path.exists() and new_path != old_path:
            messagebox.showwarning("Уже есть", "Профиль с таким названием уже существует.")
            return
        self.save(show_message=False)
        old_path.rename(new_path)
        self.reload_profiles()
        self.load_profile(clean, save_current=False)

    def delete_profile(self):
        if len(self.profiles) <= 1:
            messagebox.showwarning("Нельзя удалить", "Должен остаться хотя бы один профиль.")
            return
        name = self.active_profile
        if not messagebox.askyesno("Удалить профиль", f"Удалить профиль '{name}'?"):
            return
        self.current_profile_path.unlink(missing_ok=True)
        self.reload_profiles()
        self.load_profile(self.profiles[0], save_current=False)

    def refresh_list(self):
        self.listbox.delete(0, END)
        for item in self.items:
            self.listbox.insert(END, item)
        self.status_var.set(f"Профиль: {self.active_profile}. В списке: {len(self.items)}")

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
            messagebox.showwarning("Пустая строка", "Введите приложение, путь или ссылку.")
            return
        self.items.append(value)
        self.entry_var.set("")
        self.save(show_message=False)
        self.refresh_list()
        self.status_var.set(f"Добавлено: {value}")

    def add_link_from_dialog(self):
        value = simpledialog.askstring("Добавить ссылку", "Вставьте ссылку:", parent=self.root)
        value = normalize_item(value or "")
        if not value:
            return
        if not value.lower().startswith(("http://", "https://", "mailto:")):
            value = "https://" + value
        self.entry_var.set(value)
        self.add_item()

    def update_selected(self):
        index = self.selected_index()
        if index is None:
            messagebox.showinfo("Ничего не выбрано", "Выберите строку, которую нужно изменить.")
            return
        value = self.entry_var.get().strip()
        if not value:
            messagebox.showwarning("Пустая строка", "Введите новое значение.")
            return
        self.items[index] = value
        self.save(show_message=False)
        self.refresh_list()
        self.listbox.selection_set(index)

    def delete_selected(self):
        index = self.selected_index()
        if index is None:
            messagebox.showinfo("Ничего не выбрано", "Выберите строку для удаления.")
            return
        removed = self.items.pop(index)
        self.entry_var.set("")
        self.save(show_message=False)
        self.refresh_list()
        self.status_var.set(f"Удалено: {removed}")

    def pick_file(self):
        path = filedialog.askopenfilename(title="Выберите приложение или файл")
        if path:
            self.entry_var.set(path)

    def pick_folder(self):
        path = filedialog.askdirectory(title="Выберите папку")
        if path:
            self.entry_var.set(path)

    def save(self, show_message=True):
        write_list(self.current_profile_path, self.items)
        self.sync_legacy_config()
        self.status_var.set("Профиль сохранён")
        if show_message:
            messagebox.showinfo("Сохранено", f"Профиль сохранён: {self.active_profile}")

    def launch_selected(self):
        index = self.selected_index()
        if index is None:
            messagebox.showinfo("Ничего не выбрано", "Выберите строку для запуска.")
            return
        item = self.items[index]
        ok, error = launch_item(item)
        self.status_var.set(f"Запущено: {item}" if ok else f"Ошибка запуска: {item}")
        if not ok:
            messagebox.showerror("Ошибка запуска", error or item)

    def launch_all(self):
        if not self.items:
            messagebox.showinfo("Профиль пуст", "Добавьте хотя бы одно приложение или ссылку.")
            return

        self.save(show_message=False)
        errors = []
        for item in self.items:
            ok, error = launch_item(item)
            if not ok:
                errors.append(f"{item}: {error}")

        if errors:
            messagebox.showerror("Часть элементов не запустилась", "\n".join(errors))
            self.status_var.set(f"Запущено с ошибками: {len(errors)}")
        else:
            self.status_var.set(f"Запущен профиль '{self.active_profile}': {len(self.items)}")


def main():
    root = Tk()
    StartWorkApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

